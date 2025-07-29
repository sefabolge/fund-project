from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from funds.models import Fund

class FundAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Fund.objects.create(name="A", strategy="Equity", aum=1000)
        Fund.objects.create(name="B", strategy="Macro", aum=2000)

    def test_api_fund_list(self):
        response = self.client.get(reverse("api:fund_api_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_api_fund_filter_by_strategy(self):
        response = self.client.get(reverse("api:fund_api_list"), {"strategy": "Equity"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "A")
