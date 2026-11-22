"""Case-linked landlord research. Search excerpts are leads; documents provide evidence."""
import html
import json
import os
import re
import subprocess
from contextlib import closing
from datetime import datetime, timezone
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from discovery import address_fields, register_search
from service import connect


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def fetch(url, headers, limit, data=None):
    with build_opener(NoRedirect()).open(Request(url, headers=headers, data=data), timeout=6) as response:
        body = response.read(limit + 1)
        if len(body) > limit:
            raise ValueError("Source exceeds retrieval limit")
        return body


def trusted(url):
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    return parsed.scheme == "https" and parsed.netloc == host and (
        host.endswith((".gov.in", ".nic.in")) or host == "nsearchives.nseindia.com")


def extract(body, site):
    if body.startswith(b"%PDF"):
        raw = subprocess.run(["pdftotext","-layout","-","-"],input=body,capture_output=True,
                             check=True,timeout=6).stdout.decode()
    else:
        raw = html.unescape(re.sub("<[^>]*>", " ", body.decode(errors="replace")))
    words = set(re.findall(r"\w+",site.casefold())) - {
        "gala","plot","road","no","india","mumbai","maharashtra","warehouse","near"}
    for page, section in enumerate(raw.split("\f"),1):
        section = " ".join(section.split())
        for match in re.finditer(r"\b(?:lessor|landlord|sublessor)\b",section,re.I):
            passage = section[max(0,match.start()-180):match.end()+220]
            hits = words.intersection(re.findall(r"\w+",passage.casefold()))
            if len(hits)>=2 and any(len(token)>=4 for token in hits):
                return {"role":"Possible lessor reference","passage":passage,
                        "locator":f"PDF page {page}" if body.startswith(b"%PDF") else "Web passage"}
    return None


def search(inputs):
    site,region = inputs["site"],inputs["region"]
    findings, attempts = [], []
    if region=="Maharashtra" and re.search(r"\bmumbai\b",site,re.I) and "gala" in site.lower():
        hit=register_search(site)
        attempts.append({"source":hit["source"],"status":hit["status"]})
        if hit.get("passage"):
            findings.append({"role":"Listed business", "passage":hit["passage"],"url":hit["url"],
                             "locator":f"PDF page {hit['page']}", "fields":address_fields(hit["passage"])})
    crust_key = os.getenv("CRUSTDATA_API_KEY")
    brave_key = os.getenv("BRAVE_SEARCH_API_KEY")
    provider = "Crustdata" if crust_key or not brave_key else "Brave"
    if crust_key or brave_key:
        query = f"{site} {region} India lease lessor property owner (site:gov.in OR site:nic.in OR site:nsearchives.nseindia.com)"
        try:
            if crust_key:
                payload = json.dumps({"query": query, "location": "IN", "sources": ["web"], "page": 1}).encode()
                headers = {"Authorization": f"Bearer {crust_key}", "Content-Type": "application/json",
                           "x-api-version": "2025-11-01"}
                response = json.loads(fetch("https://api.crustdata.com/web/search/live", headers, 1_000_000, payload))
                if response.get("success") is False or response.get("metadata", {}).get("failed_pages"):
                    raise ValueError("Search incomplete")
                results = response["results"]
            else:
                params = urlencode({"q": query, "count": 5, "country": "IN"})
                response = json.loads(fetch("https://api.search.brave.com/res/v1/web/search?" + params,
                                            {"X-Subscription-Token": brave_key}, 1_000_000))
                results = response.get("web", {}).get("results", [])
            urls = list(dict.fromkeys(r["url"] for r in results if trusted(r.get("url", ""))))
            attempts.append({"source": provider, "status": f"{len(results)} search results, {len(urls)} eligible documents"})
            for url in urls[:3]:
                try:
                    evidence=extract(fetch(url,{},6_000_000),site)
                    if evidence:
                        findings.append(dict(evidence,url=url))
                    status="Matching passage" if evidence else "No qualifying passage"
                except (OSError,ValueError,subprocess.SubprocessError):
                    status="Document unavailable"
                attempts.append({"source":url,"status":status})
        except (OSError,ValueError,KeyError):
            attempts.append({"source":provider,"status":"Provider unavailable"})
    else:
        attempts.append({"source":provider,"status":"Provider key missing"})
    return {"site":site,"region":region,"checked_at":datetime.now(timezone.utc).isoformat(),
            "findings":findings,"attempts":attempts,"authority":"Unverified"}


def run_for_case(case_id, run=False):
    with closing(connect()) as db, db:
        case=db.execute("SELECT inputs FROM cases WHERE id=?",(case_id,)).fetchone()
        if not case:
            raise KeyError(case_id)
        db.execute("CREATE TABLE IF NOT EXISTS landlord_runs(case_id TEXT PRIMARY KEY, result TEXT)")
        inputs=json.loads(case[0])
        if run:
            report=search(inputs)
            db.execute("INSERT OR REPLACE INTO landlord_runs VALUES (?,?)",(case_id,json.dumps(report)))
        saved=db.execute("SELECT result FROM landlord_runs WHERE case_id=?",(case_id,)).fetchone()
        return {"inputs":inputs,"result":json.loads(saved[0]) if saved else None}
