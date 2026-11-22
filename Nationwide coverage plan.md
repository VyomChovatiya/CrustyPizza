# Nationwide warehouse diligence implementation plan amendment

Research date: 22 November 2026. Apply these changes to the seven-hour build. The ten checks and the procurement decision remain the unit of delivery.

## Four implementation changes

1. Accept every Indian state and union territory. Store the site jurisdiction independently of the landlord’s registered office and the marketing city. Dispatch lease review, occupancy calculations, identity, checklist, email and other independent checks even when a local record is missing. An unresolved mandatory parcel check yields a hold with the specific missing evidence.
2. Accept an official extract for every jurisdiction. Capture district, village or ward, survey/CTS/plot number, subdivision, issuer, record date, original language, page and source hash. Distinguish document received, identifiers matched and authenticity independently verified. Request a registered lease or allotment and signing authority where the person offering the site differs from the recorded holder. Preserve the local spelling and part-parcel suffix. Show what the document establishes and which questions remain open.
3. Route lookups through the directory below. Each adapter declares record type, local identifiers, access method, geographic coverage, last successful real test and evidence locator. Classify the attempt as retrieved, no matching record, access restricted, unsupported locality or source unavailable. For interactive portals, offer the official service and upload path. Re-evaluate only dependent checks on upload. Preserve budget, action IDs and previous report versions.
4. Publish separate coverage columns for case intake, document review and tested live retrieval. At kickoff load all 36 entries and run parameterized intake tests. In the integration block prioritize Maharashtra and Tamil Nadu, then Delhi NCR and the next client location. Promote each adapter independently after a real positive, a near-match and an outage test. A discovered URL starts with live test date unset.

## Official source directory

The national inventory below is a discovery baseline dated 8 May 2026. Rows marked “National inventory” reproduce its published RoR address, including legacy HTTP links. Resolve and confirm the current official HTTPS destination before transmitting case identifiers. Other rows identify a more specific government source. These entries have not undergone authenticated parcel retrieval. [Department of Land Resources state RoR inventory](https://dilrmp.gov.in/dilrmpold/physcial/report/pdf/stateror)

| Jurisdiction | Official starting point |
|---|---|
| ANDAMAN & NICOBAR ISLANDS | [National inventory · land records](http://db.and.nic.in/ROR/view1/formf.aspx) |
| ANDHRA PRADESH | [National inventory · land records](http://meebhoomi.ap.gov.in) |
| ARUNACHAL PRADESH | [Certificate application](https://eodb.arunachal.gov.in/services) |
| ASSAM | [National inventory · land records](http://revenueassam.nic.in) |
| BIHAR | [National inventory · land records](http://biharbhumi.bihar.gov.in) |
| CHANDIGARH | [National inventory · land records](https://revenue.chd.gov.in/) |
| CHHATTISGARH | [National inventory · land records](https://bhuiyan.cg.nic.in/) |
| GOA | [National inventory · land records](https://dslr.goa.gov.in) |
| GUJARAT | [National inventory · land records](http://anyror.gujarat.gov.in) |
| HARYANA | [Jamabandi service guide](https://ambala.gov.in/service/jamabandi-portal/) |
| HIMACHAL PRADESH | [National inventory · land records](https://himbhoomilmk.nic.in/viewlandrecords.aspx) |
| JAMMU & KASHMIR | [National inventory · land records](https://landrecords.jk.gov.in/Dashboard/Home) |
| JHARKHAND | [National inventory · land records](https://jharbhoomi.jharkhand.gov.in/) |
| KARNATAKA | [National inventory · land records](https://rdservices.karnataka.gov.in/) |
| KERALA | [Ente Bhoomi](https://revenue.entebhoomi.kerala.gov.in/) |
| LADAKH | [Land Records](https://landrecords.ladakh.gov.in/lalr/Home/) |
| LAKSHADWEEP | [Revenue Department; confirm island and extract](https://lakshadweep.gov.in/department-of-revenue/) |
| MADHYA PRADESH | [District land-record service guide](https://sidhi.nic.in/en/service/land-records/) |
| MAHARASHTRA | [National inventory · land records](https://mahabhumi.gov.in/mahabhumilink) |
| MANIPUR | [National inventory · land records](https://louchapathap.nic.in) |
| MEGHALAYA | [Revenue authority; request district record](https://www.meghalaya.gov.in/dept/39) |
| MIZORAM | [eRAM patta/application service](https://eram.mizoram.gov.in/) |
| NAGALAND | [RoR portal; confirm local coverage](https://www.lrsror.nagaland.gov.in/home) |
| NCT OF DELHI | [Indraprastha Bhulekh](https://dlrc.delhi.gov.in/) |
| ODISHA | [National inventory · land records](http://bhulekh.ori.nic.in) |
| PUDUCHERRY | [National inventory · land records](http://www.nilamagal.py.gov.in) |
| PUNJAB | [National inventory · land records](http://revenue.punjab.gov.in) |
| RAJASTHAN | [Apna Khata](https://apnakhata.rajasthan.gov.in/) |
| SIKKIM | [Reference Parcha](https://ilrms.sikkim.gov.in/Reference_Parcha.aspx) |
| TAMILNADU | [National inventory · land records](https://eservices.tn.gov.in) |
| TELANGANA | [Bhu Bharati land status](https://bhubharati.telangana.gov.in/knowLandStatus) |
| THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU | [Integrated land/property service directory](https://swp.dddgov.in/integrate-land-property-portal) |
| TRIPURA | [National inventory · land records](http://jami.tripura.gov.in) |
| UTTAR PRADESH | [National inventory · land records](http://upbhulekh.gov.in) |
| UTTARAKHAND | [National inventory · land records](https://bhulekh.uk.gov.in) |
| WEST BENGAL | [National inventory · land records](http://www.banglarbhumi.gov.in) |

## Route major city requests by parcel jurisdiction

| Client address | First lookup and required distinction |
|---|---|
| Delhi, Gurugram, Noida | Delhi revenue villages use Bhulekh and khasra details. For a registered Delhi deed collect registration year, number and subregistrar. DORIS provides historical searches and reports migration of registration offices to NGDRS. Gurugram uses Haryana and Noida uses Uttar Pradesh. For authority leasehold sites request the allotment and registered lease. [Delhi revenue](https://revenue.delhi.gov.in/revenue/land-records) · [Delhi deed search](https://edoris.delhigovt.nic.in/) |
| Mumbai, Thane, Navi Mumbai, Pune | In Mumbai City use the property-card service and match the city survey identifier. Check actual district for suburban, Thane and Navi Mumbai addresses. Use the village and Gat/subdivision for rural Pune belt sites. Ask for the industrial authority lease when relevant. [Mumbai City property card](https://mumbaicity.gov.in/en/property-card/) · [Mumbai Suburban services](https://mumbaisuburban.gov.in/en/services-2/) |
| Chennai, Hosur | Identify urban town survey ward/block or rural village and subdivision before choosing TSLR or Patta/Chitta. [Tamil Nadu land services](https://eservices.tn.gov.in/) |
| Bengaluru, Hyderabad | Bengaluru outskirts may have a survey-based RTC. For a municipal site request its property identifier and registered deed. Hyderabad parcels covered by Bhu Bharati use the district, mandal, village and survey subdivision. Confirm that the site falls in the portal’s coverage. [Karnataka land records](https://landrecords.karnataka.gov.in/service2/) · [Telangana land status](https://bhubharati.telangana.gov.in/knowLandStatus) |
| Ahmedabad, Kolkata | Select the urban property card or rural survey record according to parcel type in Gujarat. For Kolkata-area revenue plots retain mouza, khatian and dag. Municipal holding details alone leave lease authority unresolved. [Gujarat urban property service](https://e-milkat.gujarat.gov.in/) · [West Bengal land records](https://www.banglarbhumi.gov.in/) |

## Verification before release

- Run 36 intake cases with an identical lease and policy. Expect identical arithmetic, one ten-check report each and a state-specific document path. Disable the local source and verify only dependent findings change.
- Run the Maharashtra Sudhavadi Gat 200 and Tamil Nadu Anekollu 52/1 reference cases. The November filing identifies litigation at entity/location level. Require a parcel-specific order before attaching litigation to either survey number. [NSE filing, contingent liabilities](https://nsearchives.nseindia.com/corporate/NDRINVIT_03112026232107_OutcomeofBM03112026signed.pdf)
- For every added live adapter freeze a permitted dated extract and record its issuing office, local identifier and exact expected field. Replay with a changed village or subdivision and expect no match. Force an outage and expect an explicit source gap plus the correct upload request. Record portal reachability and successful parcel retrieval separately.
- Test Delhi, Gurugram and Noida with the same marketing label “Delhi NCR”. Expect three different routes. Test a Mumbai property card against a similarly numbered rural Gat and require a mismatch. For Meghalaya, exercise the authority-assisted path and require an explicit pending document. Repeat upload after a worker restart and verify one revised report and zero duplicate emails.

The competition gate is a fresh, decision-relevant source call and a reproducible evidence trail. Statewide automated retrieval is a separate claim requiring locality-specific evidence and passing tests.

