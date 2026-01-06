from django.shortcuts import render, redirect
from django.http import HttpResponse
from app_pos.forms import ProductCreateForm
from app_pos.models import Product
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def customer(request):
    return render(request, "customer.html")

@login_required(login_url="login")
def product_list(request):
    # for searching data
    if request.method == "GET" and "search" in request.GET:
        data_to_search = request.GET.get("search")
        search_data = Product.objects.filter(
            Q(product_title__icontains=data_to_search) | 
            Q(product_category__category_name__icontains=data_to_search))
        context = { "products": search_data}
    else:
        # fetching all products
        db_data = Product.objects.all()
        context = {
            "products": db_data
        }
    return render(request, "product_list.html", context)
@login_required(login_url="login")
def product_create(request):
    if request.method == "POST":
        request_data = request.POST
        db_data = ProductCreateForm(request_data)
        if db_data.is_valid():
            db_data.save()
            messages.add_message(request, messages.SUCCESS, "Product added successfully!")
            return redirect("product.list")
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!!")
            return redirect("product.create")
    create_form = ProductCreateForm()
    context = {
        "title": "Enter Your Product Details",
        "form": create_form
    }
    return render(request, "product_create.html", context)

@login_required(login_url="login")
def product_edit(request, pk):
    db_data = Product.objects.get(id=pk)
    edit_data = ProductCreateForm(instance=db_data)
    context = {"title": "Product Update", "form": edit_data}
    if request.method == "POST": 
        request_data = request.POST
        update_data = ProductCreateForm(instance=db_data, data=request_data)
        if update_data.is_valid():
            update_data.save()
            messages.add_message(request, messages.SUCCESS, "Product updated successfully!!")
            return redirect("product.list")
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!!")
            return redirect("product.edit")
    return render(request, "product_edit.html", context)

@login_required(login_url="login")
def product_detail(request, pk):
    data = Product.objects.get(id=pk)
    context = {"title": "Product Details", "data": data}
    return render(request, "product_detail.html", context)

@login_required(login_url="login")
def product_delete(request, pk):
    data = Product.objects.get(id=pk)
    try:
        data.delete()
        messages.add_message(request, messages.WARNING, "Product deleted successfully!")
        return redirect("product.list")
    except Product.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Product not found")
        return redirect("product.list")