from django.urls import path
from .views import FundUploadView,FundListView,ClearAllFundsView

app_name = "funds"

urlpatterns = [
    path('upload/', FundUploadView.as_view(), name='fund_upload'),
    path('', FundListView.as_view(), name='fund_list'),
    path("clear-funds/", ClearAllFundsView.as_view(), name="clear_funds")

    
]
