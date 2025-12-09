from django.urls import path
from app_pos.views import demo, index, customer, product

urlpatterns = [
    # Define your app-specific URL patterns here
    path('demo/', demo, name="demo"),
    path('base/', index, name="base"),
    path('customer/', customer, name="customer"),
    path('product/', product, name="product"),
]