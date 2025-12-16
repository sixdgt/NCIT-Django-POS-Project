from django.contrib import admin
from app_pos.models import Category, Product, Customer, Order, OrderItem
# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ('category_name', 'is_active', 'created_at')
    search_fields = ('category_name',)

class AdminProduct(admin.ModelAdmin):
    list_display = ('product_title', 'product_category', 'product_price', 'product_quantity', 'is_active', 'created_at')
    search_fields = ('product_title',)
    list_filter = ('product_category', 'is_active')

admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)