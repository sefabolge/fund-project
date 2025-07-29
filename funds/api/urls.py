from django.urls import path
from .views import FundListAPI, FundDetailAPI

app_name = "api"

urlpatterns = [
    path("funds/", FundListAPI.as_view(), name="fund_api_list"),
    path("funds/<int:pk>/", FundDetailAPI.as_view(), name="fund_api_detail"),
]