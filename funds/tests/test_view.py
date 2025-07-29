from django.test import TestCase
from django.urls import reverse
from funds.models import Fund

class ClearFundsViewTest(TestCase):
    def setUp(self):
        Fund.objects.create(name="A", strategy="X", aum=100)
        Fund.objects.create(name="B", strategy="Y", aum=200)

    def test_clear_funds_view(self):
        self.assertEqual(Fund.objects.count(), 2)

        response = self.client.post(reverse("funds:clear_funds"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fund.objects.count(), 0)
