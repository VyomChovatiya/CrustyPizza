# Warehouse lease diligence

An address-first review tool for an Indian 3PL procurement lead evaluating a warehouse before signing a lease. Start with the site address and its state or union territory. A landlord name is optional. The app saves a ten-check diligence file, calculates monthly base rent from a dated quote, and offers a separate search for public evidence about the lessor.

## Run locally

Use Python 3.12 or later. Install Poppler's `pdftotext` on the server for PDF evidence extraction. From the project directory, run:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app:app --host 127.0.0.1
```

Open the [local app](http://127.0.0.1:8000) or its [interactive API documentation](http://127.0.0.1:8000/docs). The prototype is designed for single-user, loopback access. SQLite stores cases and the latest discovery result in `data/cases.sqlite`. Set `DILIGENCE_DB` to use another path and reuse that path after restarting.

## Search for a landlord with Crustdata

1. Set `CRUSTDATA_API_KEY` in the environment of the process that starts Uvicorn. Restart the server after changing it. The local app requires its own server credential even if the chat connector is connected.
2. Create a case with the full site address, including the building, unit or gala number and locality. Select the property's jurisdiction. If entering a quote, supply all three fields together: area in sq ft, monthly rate in INR per sq ft, and quote date.
3. From the case report choose **Open landlord discovery**, then **Search for landlord**. The app sends the address and jurisdiction to the configured provider. Crustdata requests one India-localized page of web results per search and can consume credits. A deployment configured only with `BRAVE_SEARCH_API_KEY` uses Brave.
4. Read the extracted passage, source and page for each lead. The app attempts up to three distinct eligible HTTPS documents from Indian government, NIC or NSE archives. **Search activity** shows the provider outcome and individual document attempts. **Refresh search** runs another lookup and replaces the last discovery result for the case.

All 36 jurisdictions support intake and provider-backed search. Evidence availability varies by parcel. A public filing mentioning a lessor is a lead to check against the precise unit and current lease authority. A provider error or an empty result leaves that question open. [Crustdata Web Search reference](https://docs.crustdata.com/web-docs/search/reference.md)

## What the case report contains

- A ten-check review with outstanding evidence, a jurisdiction-specific land-record resource, and a draft landlord email. The current recommendation is **Hold**. Sending email, verifying signing authority and enforcing run budgets remain planned work.
- Monthly base rent equals area multiplied by the monthly rate. For example, 500 sq ft at ₹40 gives ₹20,000 per month. Full occupancy cost also requires contractual terms.
- For Maharashtra addresses containing Mumbai and a gala identifier, review attempts a separate lookup in the March 2024 MPCB e-waste register. A matching entry can show a listed business and address. For parcel verification, the report explains how to locate a property card using the relevant CTS number. [MPCB register](https://www.mpcb.gov.in/sites/default/files/Establishment%20of%20MPCB/Seniority%20list/2014/Authorised_E-Waste_Recyclers_%26_Refurbishers-March_2024.pdf) · [Maharashtra land records](https://bhulekh.mahabhumi.gov.in/)
- **Download case JSON** exports the case report. The separate discovery page retains its own search history for the latest run. The case report's call count and cost fields exclude that separate workflow.

## API and verification

Submit `POST /api/cases` with a UUID `request_id`, a `site`, and a `region` matching a key in [jurisdictions.json](jurisdictions.json). The response gives the case ID and report path. Identical submissions with the same request ID return the original case. Changing the inputs under that ID returns HTTP 409. Read the report with `GET /api/cases/{id}`.

```bash
.venv/bin/python -m unittest -v
```

The suite checks nationwide routing, saved reports, quote arithmetic, duplicate requests, address-passage matching and Crustdata integration with mocked provider responses. It runs without a paid search key. For a live check, submit a discovery search and inspect both the provider and document outcomes. [Nationwide coverage plan](Nationwide%20coverage%20plan.md) · [Landlord discovery plan](Landlord%20discovery%20plan.md)
