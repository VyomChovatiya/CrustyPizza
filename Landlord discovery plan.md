# Address-first landlord discovery

## Service outcome

Accept an Indian warehouse address, jurisdiction and optional commercial terms. Return the identified parcel, possible counterparties by role, the evidence for each relationship and the smallest outstanding question. The supplied landlord name is a search hint. Keep all ten existing diligence checks and the nationwide source directory. Separate land ownership, building ownership and authority to grant the proposed lease.

## Build order and decision gates

1. **Intake and existing cases.** Allow a blank landlord on both web and JSON submissions. Preserve the user's original address and commercial inputs. Add optional PIN, industrial estate, shed, unit and survey/CTS subdivision in the next schema revision. Keep original reports immutable and offer an explicit discovery run on existing cases.
2. **Resolve the physical site.** Parse the address into jurisdiction, locality, building and unit. Use a geocoder for candidate locations and record precision. Route by actual parcel jurisdiction. Search the named estate’s published plot schedules and planning or exchange filings for an address-to-parcel link. Locality-only input should still start research. If several units remain plausible, present the distinguishing plot or shed fields in one question.
3. **Discover parties without a name.** Query by address variants, parcel number and estate first. Fetch originating documents and follow recorded holder, allottee, lessor and managing entity references. Use the nationwide directory for official records, and registered lease schedules for the party entitled to let the unit. Search results, office addresses, tenant lists and broker listings can generate leads. Record their roles separately. Match a CIN or registry ID only after finding a candidate name.
4. **Decide on evidence.** For a verified lessor require a dated evidence chain connecting the requested unit to a parcel, the parcel to the named party, and that party to valid leasing authority. Preserve the exact passage, page, date, URL and subject for each link. Show joint owners, subleases, expired authority and conflicts explicitly. Area and rent can help compare listings but cannot establish identity. If a portal requires interactive access, request the specific extract and continue other checks.
5. **Run durably.** On case creation enqueue discovery in the same transaction. Key tasks by case revision, provider and normalized query. Persist search attempts, timestamps, fetched document hashes, candidates and evidence IDs before advancing. Reserve cost per call, limit concurrency, and reuse completed tasks on restart. Return distinct states for queued, searching, candidate found, verified, sources unavailable and completed without a match. Re-evaluate the recommendation after new evidence. Gate outreach to any identified party behind approval.
6. **Deliver in slices.** First connect one Maharashtra address to a dated primary filing and expose the evidence chain in the report. Next test Tamil Nadu and an ambiguous multi-unit estate. Expand direct lookup adapters jurisdiction by jurisdiction using the nationwide plan. The UI should show candidate names with roles, identifiers and decisive source passages beside the missing link; polling must preserve keyboard focus.

## Acceptance suite

| Input | Required result |
|---|---|
| Saved Vikhroli case, remove Godrej hint, keep 1,000 sq ft and ₹50 | ₹50,000 monthly base rent; neighborhood alone cannot identify a unique lessor. If the search finds a company office there, retain only the evidenced office role. |
| Sudhavadi, Maval, Gat 188/189, deed excerpt clause 2 in the [NSE-filed valuation](https://nsearchives.nseindia.com/corporate/NDRINVIT_18032026152709_BMOutcome18032026.pdf) | Retrieve the correct parcel schedule and dated ground lease. Keep the ground lessor and warehouse subletting authority separate. Substitute Gat 200 and confirm the first deed cannot settle the second request. |
| Anekollu, subdivision 52/1, [Tamil Nadu environmental minutes](https://environmentclearance.nic.in/writereaddata/FormB/agenda/2107202519088936850thSEIAASIGNEDMINUTES.pdf) | Extract NDR Unique Space as project proponent with its passage. The environmental proposal alone leaves leasing authority unresolved. |
| Same property listed by two brokers, changed price, duplicate source and interrupted worker | One parcel and distinct party roles; price change cannot switch the lessor. Resume within the original budget and send zero emails. |
| Confirmed lessor positive control | Before promoting an adapter, manually label a dated executed warehouse lease identifying the exact unit, contracting lessor and authority, then withhold the name from intake. Require the same legal party, valid dates and independently inspected citations. |
| Portal outage or ambiguous unit | State which source failed or which identifier distinguishes candidates. Preserve all successful independent findings. |

Release gate: reproduce all expected roles and abstentions on pinned records, prove one live address-led retrieval on an unseen case, and reject all unsupported lessor attributions. Report successful identification rate separately from evidence accuracy and provider availability.
