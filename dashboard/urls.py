from django.urls import path
from dashboard.views import *

urlpatterns = [
    path("", DashboardView, name="dashboard"),
    path("bidding/", BiddingView.as_view(), name="bidding"),
    path("bidding/<int:pk>/download/", DownloadExcellView),
]
