from django.shortcuts import render
from django.http import HttpResponse
from app_pos.forms import ProductCreateForm
# Create your views here.
def demo(request):
    return HttpResponse("This is a demo view from app_pos.")

def index(request):
    return render(request, "base.html")

def customer(request):
    return render(request, "customer.html")

def product(request):
    context = {
        'product_name': 'Wireless Mouse',
        'price': 25.99,
        'description': 'A high-precision wireless mouse with ergonomic design.'
    }
    return render(request, "product.html", context)

def product_create(request):
    create_form = ProductCreateForm()
    context = {
        "title": "Enter Your Product Details",
        "form": create_form
    }
    return render(request, "product_create.html", context)
