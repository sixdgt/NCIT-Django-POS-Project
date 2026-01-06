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

def register_view(request):
    if request.method == "POST":
        # taking inputs from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, "Password and Confirm Password do not match!!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username already taken!!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "Email already registered!!")
            return redirect("register")
        try:
            user = User.objects.create_user(first_name=first_name, 
                                            last_name=last_name, email=email,
                                              username=username, password=password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Registration successful!! Please login.")
            return redirect("login")
        except:
            messages.add_message(request, messages.ERROR, "Registration failed!! Username may already exist.")
            return redirect("register")
    return render(request, "register.html")

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logged out successfully!!")
    return redirect("login")

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, "dashboard.html")
