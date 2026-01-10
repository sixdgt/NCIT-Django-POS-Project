from django import forms
from app_pos.models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_title', 'product_category', 'product_price', 'product_description', 'product_quantity']
        
        widgets = {
            "product_title": forms.TextInput(attrs={
                "class": "form-control form-control-lg mb-2", 
                "placeholder": "Enter Title"
            }),
            "product_category": forms.Select(attrs={
                "class": "form-select form-control-lg mb-2"
            }),
            "product_price": forms.NumberInput(attrs={
                "class": "form-control form-control-lg mb-2", 
                "placeholder": "0.00"
            }),
            "product_description": forms.Textarea(attrs={
                "class": "form-control mb-2", 
                "placeholder": "Describe the product...",
                "rows": 4
            }),
            "product_quantity": forms.NumberInput(attrs={
                "class": "form-control form-control-lg mb-2", 
                "placeholder": "0"
            }),
        }
        
        labels = {
            "product_title": "Product Title",
            "product_category": "Product Category",
            "product_price": "Product Price",
            "product_description": "Product Description",
            "product_quantity": "Product Quantity",
        }