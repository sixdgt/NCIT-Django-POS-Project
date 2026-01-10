from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from app_pos.models import Product
from django.contrib import messages
from django.db import transaction # Important for data safety
from .models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count

@login_required(login_url="login")
def pos_receipt(request, sale_id):
    # Fetch the specific sale using the ID from the URL
    sale = get_object_or_404(Sale, id=sale_id)
    
    context = {
        "sale": sale,
    }
    return render(request, "sales/pos_receipt.html", context)

@login_required(login_url='login')
def sales_report(request):
    today = timezone.now().date()
    
    # Filter sales for today
    today_sales = Sale.objects.filter(transaction_date__date=today)
    
    # Metrics
    total_revenue = today_sales.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    total_transactions = today_sales.count()
    items_sold = SaleItem.objects.filter(sale__in=today_sales).aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    # Data for the Table (Recent Sales)
    recent_sales = today_sales.order_by('-transaction_date')[:10]
    
    context = {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'items_sold': items_sold,
        'recent_sales': recent_sales,
        'today': today,
    }
    return render(request, 'sales/sales_report.html', context)

@login_required(login_url='login')
def transaction_history(request):
    query = request.GET.get('search_invoice')
    if query:
        # Search by Invoice ID or Customer Name
        sales = Sale.objects.filter(id__icontains=query).order_by('-transaction_date')
    else:
        sales = Sale.objects.all().order_by('-transaction_date')

    context = {
        'sales': sales,
        'search_query': query
    }
    return render(request, 'sales/transaction_history.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Use string key for session consistency
    p_id = str(product_id)
    
    current_qty_in_cart = cart.get(p_id, {}).get('quantity', 0)

    # 1. Check if we have enough stock before adding
    if product.product_quantity > current_qty_in_cart:
        if p_id in cart:
            cart[p_id]['quantity'] += 1
            messages.info(request, f"Updated quantity for {product.product_title}")
        else:
            cart[p_id] = {'quantity': 1}
            messages.success(request, f"{product.product_title} added to cart")
    else:
        messages.warning(request, f"Sorry, only {product.product_quantity} units of {product.product_title} available.")
    
    request.session['cart'] = cart
    # Tell Django the session was modified
    request.session.modified = True 
    return redirect('pos.register')

@login_required(login_url='login')
def checkout(request):
    if request.method != "POST":
        return redirect('pos.register')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('pos.register')

    discount = float(request.POST.get('discount_input', 0) or 0)
    tax_rate = 0.10 

    try:
        with transaction.atomic():
            # Calculate Subtotal
            temp_subtotal = 0
            for p_id, item_data in cart.items():
                product = Product.objects.get(id=p_id)
                temp_subtotal += float(product.product_price) * item_data['quantity']

            tax_val = temp_subtotal * tax_rate
            final_total = (temp_subtotal + tax_val) - discount

            # 1. Create the Sale first
            new_sale = Sale.objects.create(
                subtotal=temp_subtotal,
                tax_amount=tax_val,
                discount_amount=discount,
                grand_total=final_total
            )

            # 2. Create SaleItems and LINK them to the sale
            for p_id, item_data in cart.items():
                product = Product.objects.get(id=p_id)
                qty = item_data['quantity']
                
                # Check stock one last time
                if product.product_quantity < qty:
                    raise Exception(f"Insufficient stock for {product.product_title}")

                SaleItem.objects.create(
                    sale=new_sale, # <--- THIS LINKS IT TO THE RECEIPT
                    product=product,
                    quantity=qty,
                    unit_price=product.product_price,
                    total_price=float(product.product_price) * qty
                )

                # Deduct stock
                product.product_quantity -= qty
                product.save()

            # 3. Clear session
            del request.session['cart']
            request.session.modified = True
            
            return redirect('pos.receipt', sale_id=new_sale.id)

    except Exception as e:
        messages.error(request, f"Transaction Failed: {str(e)}")
        return redirect('pos.register')

@login_required(login_url='login')
def pos_register(request):
    # Get cart from session or empty dict if it doesn't exist
    cart = request.session.get('cart', {})
    cart_items = []
    total_bill = 0

    # Transform session data into product objects for the template
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.product_price * item_data['quantity']
        total_bill += subtotal
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total_bill': total_bill,
        'products': Product.objects.all() # To pick products from
    }
    return render(request, 'sales/pos_register.html', context)

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    if p_id in cart:
        del cart[p_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.warning(request, "Item removed from cart")
    return redirect('pos.register')

@login_required(login_url='login')
def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('pos.register')
