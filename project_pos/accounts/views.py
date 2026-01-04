from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def login_view(request):
    if request.method == "POST":
        # taking inputs from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(login, username=username, password=password)
        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Login successful!!")
            return redirect("dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Login failed!!")
            return redirect("login")
    return render(request, "login.html")