from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import get_user_model, login

User = get_user_model()

class SignupView(View):
    def get(self, request):
        return render(request, "registration/signup.html")

    def post(self, request):
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(username, email, password)
        user.save()

        login(request, user)

        return redirect("/")
