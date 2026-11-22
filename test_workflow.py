import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from service import REGIONS, create, review

class WorkflowTests(unittest.TestCase):
    def test_national_intake_and_restart(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, DILIGENCE_DB=str(Path(folder)/"cases.db")):
            self.assertEqual(len(REGIONS),36)
            for region in REGIONS:
                data = dict(region=region,landlord="Test lessor",site="Test site",area="50000",rate="28",quote_date="2026-10-01")
                token = str(uuid4())
                key = create(token,data)
                result = review(key)
                self.assertEqual(len(result["findings"]),10)
                self.assertIn("1,400,000.00",result["findings"]["Occupancy cost"]["detail"])
                self.assertEqual(result["recommendation"],"Hold")
                if region == "Maharashtra":
                    self.assertIn("CTS",result["parcel_source"]["instructions"])
                else:
                    self.assertEqual(result["parcel_source"],REGIONS[region])
                self.assertEqual(create(token,data),key)
                self.assertEqual(review(key),result)
                with self.assertRaises(ValueError):
                    create(token,{**data,"site":"Changed site"})
