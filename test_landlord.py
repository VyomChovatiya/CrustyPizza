import unittest
from unittest.mock import patch
from landlord import extract, search, trusted

class LandlordDiscoveryTests(unittest.TestCase):
    def test_document_and_address_must_overlap(self):
        content=b"<p>Example Estates Ltd is the lessor of Unit 5 at Gilbert Compound.</p>"
        self.assertIn("Example Estates", extract(content,"Gilbert Compound, Mumbai")["passage"])
        self.assertIsNone(extract(content,"Unit 18, Ambattur"))

    def test_sources_and_missing_provider(self):
        self.assertFalse(trusted("https://nseindia.com.example.org/doc"))
        self.assertTrue(trusted("https://nsearchives.nseindia.com/doc"))
        with patch.dict("os.environ",{"BRAVE_SEARCH_API_KEY":"","CRUSTDATA_API_KEY":""}):
            result=search({"region":"Delhi","site":"Okhla"})
        self.assertEqual(result["authority"],"Unverified")
        self.assertEqual(result["attempts"][0]["status"],"Provider key missing")

    def test_crustdata_search_and_document_extraction(self):
        import json
        from service import REGIONS
        site = "Gilbert Compound"
        url = "https://example.gov.in/deed"
        for region in REGIONS:
            with patch.dict("os.environ", {"CRUSTDATA_API_KEY":"test","BRAVE_SEARCH_API_KEY":"unused"}), patch("landlord.fetch") as fetch:
                fetch.side_effect = [json.dumps({"success":True,"results":[{"url":url}]}).encode(),
                                     b"Gilbert Compound lease identifies Example Estates as lessor."]
                report = search({"site":site,"region":region})
                endpoint, headers, _, body = fetch.call_args_list[0].args
                self.assertEqual(endpoint,"https://api.crustdata.com/web/search/live")
                self.assertEqual(headers["Authorization"],"Bearer test")
                self.assertIn(region,json.loads(body)["query"])
                self.assertEqual(report["findings"][0]["url"],url)
                self.assertEqual(fetch.call_args_list[1].args[1],{})
