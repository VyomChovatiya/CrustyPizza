"""Search the public MPCB register for address leads in Mumbai industrial units."""
import re
import subprocess
from datetime import datetime, timezone
from urllib.request import Request, urlopen

REGISTER = "https://www.mpcb.gov.in/sites/default/files/Establishment%20of%20MPCB/Seniority%20list/2014/Authorised_E-Waste_Recyclers_%26_Refurbishers-March_2024.pdf"

def compact(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())

def address_fields(passage):
    """Extract only values present in the matched register passage."""
    text = " ".join(passage.split())
    start = re.search(r"\bgala\s*(?:no\.?\s*)?\d+", text, re.I)
    if not start:
        return {}
    fields = {"Registered site address": text[start.start():]}
    organisation = text[:start.start()].strip(" ,:-")
    if organisation and any(c.isalpha() for c in organisation):
        fields["Listed business"] = organisation
    return fields

def register_search(site):
    result = {"url": REGISTER, "source": "MPCB authorised e-waste register, March 2024",
              "attempted_at": datetime.now(timezone.utc).isoformat(), "status": "Source unavailable"}
    try:
        with urlopen(Request(REGISTER, headers={"User-Agent":"WarehouseDiligence/1.0"}), timeout=7) as response:
            pdf = response.read(8_000_001)
        if len(pdf) > 8_000_000 or not pdf.startswith(b"%PDF"):
            return result
        raw = subprocess.run(["pdftotext","-raw","-","-"], input=pdf, capture_output=True, timeout=8, check=True).stdout.decode("utf8")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        result["error"] = type(error).__name__
        return result
    unit = re.search(r"\bgala\s*(?:no\.?\s*)?(\d+)\b",site,re.I)
    compound = re.search(r"\b([\w'-]+)\s+compound\b",site,re.I)
    result["status"] = "No matching register entry"
    if not unit or not compound:
        return result
    for page, content in enumerate(raw.split("\f"),1):
        for match in re.finditer(r"\bgala\s*(?:no\.?\s*)?0*" + str(int(unit[1])) + r"\b",content,re.I):
            window = content[match.start():match.end()+120]
            if compact(compound[0]) in compact(window) and "mumbai" in compact(window):
                line_start = content.rfind("\n", 0, match.start()) + 1
                end = re.search(r"\bmumbai\b", window, re.I)
                stop = match.start() + end.end() if end else match.end()
                result.update(status="Address lead",page=page,passage=content[line_start:stop].strip())
                return result
    return result
