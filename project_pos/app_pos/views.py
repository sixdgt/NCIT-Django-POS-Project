from django.shortcuts import render, redirect
from django.http import HttpResponse
from app_pos.forms import ProductCreateForm
from app_pos.models import Product
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def landing(request):
    return render(request, "landing.html")

@login_required(login_url="login")
def product_list(request):
    # Search logic
    if request.method == "GET" and "search" in request.GET:
        data_to_search = request.GET.get("search")
        products_list = Product.objects.filter(
            Q(product_title__icontains=data_to_search) | 
            Q(product_category__category_name__icontains=data_to_search)
        ).order_by('-id')
    else:
        products_list = Product.objects.all().order_by('-id')

    # Pagination Logic
    paginator = Paginator(products_list, 5) # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
    }
    return render(request, "product_list.html", context)

@login_required(login_url="login")
def product_create(request):
    form = ProductCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("product.list")
        messages.error(request, "Please correct the errors below.")
    
    context = {
        "title": "Add New Product",
        "form": form,
        "button_text": "Save Product"
    }
    return render(request, "product_form.html", context)

@login_required(login_url="login")
def product_edit(request, pk):
    product = Product.objects.get(id=pk)
    # Pass instance to the form for both GET and POST
    form = ProductCreateForm(request.POST or None, instance=product)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product.list")
        messages.error(request, "Update failed. Check your input.")

    context = {
        "title": f"Update: {product.product_title}",
        "form": form,
        "button_text": "Update Product"
    }
    return render(request, "product_form.html", context)

@login_required(login_url="login")
def product_detail(request, pk):
    data = Product.objects.get(id=pk)
    context = {"title": "Product Details", "data": data}
    return render(request, "product_detail.html", context)

@login_required(login_url="login")
def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == "POST":
        product.delete()
        messages.warning(request, "Product deleted successfully!")
        return redirect("product.list")
    
    # This renders the "Are you sure?" page we built earlier
    return render(request, "product_delete.html", {"data": product})