from django.urls import path
from pos_api.views import (ProductListCreateApiView, ProductDetailUpdateDeleteApiView)

urlpatterns = [
    # API URL patterns will be defined here
    path('product-list-create/', ProductListCreateApiView.as_view()),
    path('product-detail-delete-update/<int:pk>/', ProductDetailUpdateDeleteApiView.as_view())
]