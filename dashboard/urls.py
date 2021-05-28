from django.urls import path
from dashboard.views import BiddingView, DashboardView

urlpatterns = [
    path("", DashboardView, name="dashboard"),
    path("bidding/", BiddingView, name="bidding"),
]
