from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == "teacher":
                return redirect("teacher_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            messages.error(request, "Username yoki parol noto‘g‘ri")
            return redirect("login")



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

