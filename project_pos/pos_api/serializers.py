from rest_framework import serializers
from app_pos.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_title', 'product_category', 'product_price',\
                  'product_description', 'product_quantity', 'cost_price']