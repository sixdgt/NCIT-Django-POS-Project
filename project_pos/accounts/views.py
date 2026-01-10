from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from app_pos.models import Product
from app_sales.models import Sale, SaleItem
from django.db.models import Sum
from django.utils import timezone

# Create your views here.
def send_custom_email(request, subject, message, recipient_list):
    try:
        send_mail(
            subject, # email subject
            message, # email body
            settings.EMAIL_HOST_USER, #sender email
            recipient_list, # receiver email
            fail_silently=False
        )
        # this message depends on various cases; don't send unless its verification email/password reset/etc.
        messages.add_message(request, messages.SUCCESS, "Email sent successfully!")
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"Failed to send email: {e}")

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
            # sending email
            send_custom_email(
                request,
                'Account Creation',
                'Your account has been created successfully.',
                [email]
            )
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
    today = timezone.now().date()
    
    # 1. Calculate Statistics
    total_revenue = Sale.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    orders_today = Sale.objects.filter(transaction_date__date=today).count()
    total_products = Product.objects.aggregate(Sum('product_quantity'))['product_quantity__sum'] or 0
    
    # 2. Get Recent Transactions
    recent_transactions = Sale.objects.order_by('-transaction_date')[:5]
    
    # 3. Low Stock Alerts
    low_stock_products = Product.objects.filter(product_quantity__lt=5)
    
    context = {
        'total_revenue': total_revenue,
        'orders_today': orders_today,
        'total_products': total_products,
        'recent_transactions': recent_transactions,
        'low_stock_products': low_stock_products,
        'low_stock_count': low_stock_products.count(),
    }
    return render(request, "dashboard.html", context)
