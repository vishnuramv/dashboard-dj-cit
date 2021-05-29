from dashboard.models import Bidding, BiddingRow
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def DashboardView(request):
    user = request.user

    total_mw = 0
    biddings = Bidding.objects.filter(owner=user)
    for bidding in biddings:
        total_mw += bidding.total_qty

    return render(request, "dashboard/index.html", {"total_mw": total_mw})


class BiddingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "bidding/index.html", {"dummy_arr": list(range(10))})

    def post(self, request):
        bidding = Bidding()
        bidding.owner = request.user
        bidding.total_price = 0
        bidding.total_qty = 0
        bidding.save()

        total_qty = 0
        total_price = 0

        for i in range(10):
            data = {
                "slot": request.POST[f"slot_{i}"],
                "from": request.POST[f"from_{i}"],
                "to": request.POST[f"to_{i}"],
                "block": request.POST[f"block_{i}"],
                "quantity": request.POST[f"quantity_{i}"],
                "price": request.POST[f"price_{i}"],
            }

            if all(data.values()):
                row = BiddingRow()

                row.slot = data["slot"]
                hr, min = map(int, data["from"].split(":"))
                row.from_time = datetime.time(hr, min)
                hr, min = map(int, data["to"].split(":"))
                row.to_time = datetime.time(hr, min)
                row.time_block = data["block"]
                row.quantity = int(data["quantity"])
                row.price = int(data["price"])
                row.bidding = bidding

                row.save()

                total_price += row.quantity * row.price
                total_qty += row.quantity

        bidding.total_price = total_price
        bidding.total_qty = total_qty
        bidding.save()

        return render(
            request,
            "bidding/index.html",
            {"dummy_arr": list(range(10)), "message": "Bidding Saved"},
        )
