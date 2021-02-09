from rest_framework import serializers
from .models import Product, Wishlist


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WishlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'  # ['title', 'products']




