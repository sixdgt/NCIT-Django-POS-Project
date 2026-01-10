from django.urls import path
from . import views

urlpatterns = [
    path('pos/', views.pos_register, name="pos.register"),
    path('pos/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('pos/clear/', views.clear_cart, name="clear_cart"),
    path('pos/checkout/', views.checkout, name="pos.checkout"),
    path('pos/receipt/<int:sale_id>/', views.pos_receipt, name="pos.receipt"),
    path('sales/report/', views.sales_report, name="sales.report"),
    path('pos/remove/<int:product_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('transactions/', views.transaction_history, name="sales.history"),
]