"""Case workflow. All findings in a report are committed together."""
import json
import os
import sqlite3
from contextlib import closing
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from discovery import address_fields, register_search

ROOT = Path(__file__).resolve().parent
REGIONS = json.loads((ROOT / "jurisdictions.json").read_text())
CHECKS = {
    "Landlord": "Dated registration and authority to lease",
    "Directors": "Dated role and identity-matched screening records",
    "Listing claims": "Listing and independent supporting passages",
    "Disputes": "Parcel identifiers and relevant records",
    "Neighborhood rent": "Dated local comparable leases",
    "Lease clauses": "Draft lease with page and clause references",
    "Occupancy cost": "Contractual rent, term, escalation and deposit",
    "Connectivity": "Site entrance and dated route response",
    "Labor ecosystem": "Geolocated, dated employer and vacancy records",
    "Compliance": "Client checklist and matching documents",
}

def connect():
    path = Path(os.environ.get("DILIGENCE_DB", ROOT / "data" / "cases.sqlite"))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS cases
        (id TEXT PRIMARY KEY, request_id TEXT UNIQUE, inputs TEXT NOT NULL,
         report TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return db

def create(request_id, inputs):
    payload = json.dumps(inputs, sort_keys=True)
    with closing(connect()) as db, db:
        db.execute("INSERT INTO cases(id,request_id,inputs) VALUES(?,?,?) ON CONFLICT(request_id) DO NOTHING",
                   (str(uuid4()), request_id, payload))
        key, original = db.execute("SELECT id,inputs FROM cases WHERE request_id=?", (request_id,)).fetchone()
        if original != payload:
            raise ValueError("Request ID already belongs to different inputs.")
    return key

def add_address_evidence(report):
    attempt = report.get("address_search", {})
    if attempt.get("passage"):
        attempt["fields"] = address_fields(attempt["passage"])
        business = attempt["fields"].get("Listed business")
        if business:
            report["findings"]["Landlord"]["detail"] = (
                f"{attempt['source']} lists {business} at this address (page {attempt['page']}). "
                "The property card and unit-specific lease authority are still outstanding."
            )
    return report

def review(key):
    with closing(connect()) as db, db:
        row = db.execute("SELECT inputs,report FROM cases WHERE id=?", (key,)).fetchone()
        if not row:
            raise KeyError(key)
        if row[1]:
            existing = json.loads(row[1])
            if existing.get("lookup_version") or existing["inputs"]["region"] != "Maharashtra":
                return add_address_evidence(existing)
        inputs = json.loads(row[0])
        findings = {name: {"status":"Cannot verify","detail":missing} for name, missing in CHECKS.items()}
        area, rate = inputs.get("area"), inputs.get("rate")
        if area and rate:
            monthly = Decimal(area) * Decimal(rate)
            findings["Occupancy cost"] = {
                "status":"Partial", "detail":f"Monthly base rent ₹{monthly:,.2f}. Full-term cost requires lease terms.",
                "basis":{"source":"Submitted quote","fields":["area","rate"],"formula":"area in sq ft × monthly INR per sq ft","date":inputs["quote_date"]}}
        report = dict(id=key, inputs=inputs, recommendation="Hold", reason="Mandatory evidence is outstanding.",
                      findings=findings, parcel_source=REGIONS[inputs["region"]], ledger={"calls":0,"cost_inr":0},
                      email_draft=f"Please provide the current parcel extract, draft lease and evidence of authority to lease the site at {inputs['site']}.",
                      action_status="Draft",live_retrieval="Untested")
        if inputs["region"] == "Maharashtra":
            report["lookup_version"] = 1
            report["parcel_source"] = {
                "service": "Maharashtra Bhulekh · View land record",
                "url": "https://bhulekh.mahabhumi.gov.in/",
                "instructions": "For urban land select Property Card, then the district, survey office or village and CTS number from the property papers. For rural land choose 7/12 and the village and survey/Gat number. If only a street address is available, obtain the parcel identifier from the registered deed or City Survey Office. A gala number identifies a unit within a building."
            }
            if "mumbai" in inputs["site"].lower() and "gala" in inputs["site"].lower():
                attempt = register_search(inputs["site"])
                report["address_search"] = attempt
                report["ledger"]["calls"] = 1
                report["live_retrieval"] = attempt["status"]
                findings["Landlord"]["detail"] = f'MPCB address search: {attempt["status"]}. Establish the lessor with the property card and a deed or authority covering this unit.'
        add_address_evidence(report)
        db.execute("UPDATE cases SET report=? WHERE id=?", (json.dumps(report), key))
        return report
