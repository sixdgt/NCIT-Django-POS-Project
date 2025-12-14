from django import forms
from app_pos.models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_title','product_category','product_price', 'product_description', 'product_quantity']
        widgets = {
            "product_title": forms.TextInput(attrs={"class":"form-control mb-2", 
                                                    "placeholder":"Enter Product Title"}),
            "product_category": forms.Select(attrs={"class":"form-control mb-2", 
                                                       "placeholder":"Enter Product Category"}),
            "product_price": forms.NumberInput(attrs={"class":"form-control mb-2", 
                                                      "placeholder":"Enter Product Price"}),
            "product_description": forms.Textarea(attrs={"class":"form-control mb-2",
                                                          "placeholder":"Enter Product Description", "rows": 3}),
            "product_quantity": forms.NumberInput(attrs={"class":"form-control mb-2",
                                                          "placeholder":"Enter Product Quantity"}),

        }
        labels = {
            "product_title": "Product Title",
            "product_category": "Product Category",
            "product_price": "Product Price",
            "product_description": "Product Description",
            "product_quantity": "Product Quantity",
        }