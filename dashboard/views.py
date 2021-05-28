from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def DashboardView(request):
    return render(request, "dashboard/index.html")


@login_required
def BiddingView(request):
    return render(request, "bidding/index.html", {"dummy_arr": list(range(10))})
