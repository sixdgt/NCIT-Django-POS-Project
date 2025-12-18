from django.shortcuts import render, redirect
from django.http import HttpResponse
from app_pos.forms import ProductCreateForm
from app_pos.models import Product
# Create your views here.
def customer(request):
    return render(request, "customer.html")

def product_list(request):
    # fetching all products
    db_data = Product.objects.all()
    context = {
        "products": db_data
    }
    return render(request, "product_list.html", context)
def product_create(request):
    if request.method == "POST":
        request_data = request.POST
        db_data = ProductCreateForm(request_data)
        if db_data.is_valid():
            db_data.save()
            return redirect("product.list")
        else:
            return redirect("product.create")
    create_form = ProductCreateForm()
    context = {
        "title": "Enter Your Product Details",
        "form": create_form
    }
    return render(request, "product_create.html", context)