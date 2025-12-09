from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ELEC', 'Electronics'),
        ('FASH', 'Fashion'),
        ('HOME', 'Home & Living'),
        ('BOOK', 'Books'),
        ('OTHR', 'Other'),
    ]
    product_title = models.CharField(max_length=200, null=False, blank=False)
    product_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False, blank=False)
    product_price = models.FloatField(null=False, blank=False)
    product_description = models.TextField(null=True, blank=True)
    product_quantity = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.product_title