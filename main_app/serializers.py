from rest_framework import serializers
from .models import Product, Category, Manufacturer, ShoppingCart, ShoppingCartElement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = ShoppingCart
        fields = '__all__'

class ShoppingCartElementSerializer(serializers.ModelSerializer):
    shopping_cart = ShoppingCartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = ShoppingCartElement
        fields = '__all__'