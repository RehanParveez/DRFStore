from rest_framework import serializers
from stores.models import Store, Category, Product
from accounts.serializers import UsersSerializers

class StoreSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'city']
        
class ProductSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']

class StoreSerializers(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    products = ProductSerializer1(many=True, read_only=True)
    owner = UsersSerializers(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'name', 'city', 'owner', 'created_at', 'product_count', 'products']
        
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        
class ProductsSerializers(serializers.ModelSerializer):
    store = StoreSerializer1(read_only=True)
    category = CategorySerializers(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'store', 'category', 'created_at']