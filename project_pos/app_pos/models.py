from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, null=False, blank=False)
    category_description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_title = models.CharField(max_length=200, null=False, blank=False)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                          null=False, blank=False)
    product_price = models.FloatField(null=False, blank=False)
    product_description = models.TextField(null=True, blank=True)
    product_quantity = models.IntegerField(null=False, blank=False, default=0)
    cost_price = models.FloatField(null=False, blank=False, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.product_title

class Customer(models.Model):
    customer_name = models.CharField(max_length=200, null=False, blank=False)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.customer_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                  null=False, blank=False)
    order_code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    order_date = models.DateTimeField(default=timezone.now())
    total_amount = models.FloatField(null=False, blank=False, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"Order #{self.id} - {self.customer.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"{self.product.product_title} x {self.quantity} for Order #{self.order.id}"