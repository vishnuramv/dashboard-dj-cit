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

        user_with_username = User.objects.filter(username=username)
        if user_with_username.exists():
            return render(request, "registration/signup.html", { "error": "Username Already Taken" })

        user_with_email = User.objects.filter(email=email)
        if user_with_email.exists():
            return render(request, "registration/signup.html", { "error": "Email Already Exists" })

        if len(password) < 5:
            return render(request, "registration/signup.html", { "error": "Password is too weak" })

        user = User.objects.create_user(username, email, password)
        user.save()

        login(request, user)

        return redirect("/")
