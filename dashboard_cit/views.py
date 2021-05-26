from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def SignupView(request):
    print("hello")
    return render(request, "signup.html")
