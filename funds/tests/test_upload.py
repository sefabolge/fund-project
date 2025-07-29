import io
from django.test import TestCase
from django.urls import reverse
from funds.models import Fund

class FundUploadTest(TestCase):
    def upload_csv(self, csv_content, filename="test.csv"):
        file = io.StringIO(csv_content)
        file.name = filename
        return self.client.post(reverse("funds:fund_upload"), {"csv_file": file}, format="multipart")

    def test_upload_and_deduplicate(self):
        initial_csv = """Name,Strategy,AUM (USD),Inception Date
Test Fund A,Equity,1000000,2020-01-01
Test Fund B,Macro,2000000,2021-02-02
"""
        response = self.upload_csv(initial_csv)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fund.objects.count(), 2)

        # Upload same file again (should deduplicate)
        response = self.upload_csv(initial_csv)
        self.assertEqual(Fund.objects.count(), 2)

        # Upload overlapping update
        updated_csv = """Name,Strategy,AUM (USD),Inception Date
Test Fund A,Equity,9000000,2020-01-01
New Fund C,Equity,1500000,2023-03-03
"""
        response = self.upload_csv(updated_csv, filename="update.csv")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fund.objects.count(), 3)

        # Ensure Fund A was updated
        fund_a = Fund.objects.get(name="Test Fund A")
        self.assertEqual(fund_a.aum, 9000000)
