from django import forms
from app_pos.models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_title','product_category','product_price', 'product_description', 'product_quantity']