from django.urls import path
from app_pos.views import customer, product_list, product_create

urlpatterns = [
    # Define your app-specific URL patterns here
    path('customer/', customer, name="customer"),
    path('product/list/', product_list, name="product.list"),
    path('product/create/', product_create, name="product.create"),
]