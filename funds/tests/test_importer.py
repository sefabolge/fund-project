import io
from django.test import TestCase
from funds.models import Fund
from funds.services.fund_importer import import_funds_from_csv

class FundImporterTest(TestCase):
    def test_import_creates_funds(self):
        csv_data = """Name,Strategy,AUM (USD),Inception Date
Test Fund A,Long/Short Equity,1000000,2022-01-01
Test Fund B,Global Macro,2000000,2023-02-02
"""
        f = io.StringIO(csv_data)
        created, updated = import_funds_from_csv(f)  

        self.assertEqual(created, 2)
        self.assertEqual(updated, 0)
        self.assertEqual(Fund.objects.count(), 2)
        self.assertTrue(Fund.objects.filter(name="Test Fund A").exists())
