from dashboard.models import Bidding, BiddingRow
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import xlsxwriter


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

        if "excel" in request.POST:
            # create a excel file and send to user
            return redirect(f"/bidding/{bidding.id}/download/")

        return render(
            request,
            "bidding/index.html",
            {"dummy_arr": list(range(10)), "message": "Bidding Saved"},
        )


@login_required
def DownloadExcellView(request, pk):
    user = request.user
    bidding = Bidding.objects.get(pk=pk)

    workbook = xlsxwriter.Workbook(f"media/files/{user.username}-Bidding.xlsx")
    worksheet = workbook.add_worksheet()
    heading_format = workbook.add_format({"bold": True})

    worksheet.write("A1", "Slot", heading_format)
    worksheet.write("B1", "From", heading_format)
    worksheet.write("C1", "To", heading_format)
    worksheet.write("D1", "Time Block", heading_format)
    worksheet.write("E1", "Buy Quantity", heading_format)
    worksheet.write("F1", "Price", heading_format)

    rows = BiddingRow.objects.filter(bidding=bidding)
    row_index = 2

    for row in rows:
        worksheet.write(f"A{row_index}", row.slot)
        worksheet.write(f"B{row_index}", row.from_time)
        worksheet.write(f"C{row_index}", row.to_time)
        worksheet.write(f"D{row_index}", row.time_block)
        worksheet.write(f"E{row_index}", row.quantity)
        worksheet.write(f"F{row_index}", row.price)

        row_index += 1

    worksheet.write(f"D{row_index}", "TOTAL")
    worksheet.write(f"E{row_index}", f"=SUM(E2:E{row_index - 1})")
    worksheet.write(f"F{row_index}", f"=SUM(F2:F{row_index - 1})")

    workbook.close()

    response = HttpResponse(workbook)
    response[
        "Content-Disposition"
    ] = f"attachment; filename={user.username}-Bidding.xlsx"
    return response
