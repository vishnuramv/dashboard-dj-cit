from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def DashboardView(request):
    return render(request, "index.html")
