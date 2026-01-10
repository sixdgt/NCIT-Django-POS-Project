from django.urls import path
from app_pos.views import product_list, product_create, product_edit, product_delete, product_detail

urlpatterns = [
    # product CRUD
    path('product/list/', product_list, name="product.list"),
    path('product/create/', product_create, name="product.create"),
    path('product/edit/<int:pk>/', product_edit, name="product.edit"),
    path('product/detail/<int:pk>/', product_detail, name="product.detail"),
    path('product/delete/<int:pk>/', product_delete, name="product.delete")
]