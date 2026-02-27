from rest_framework import serializers
from stores.models import Store, Category, Product

class StoreSerializers(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Store
        fields = ['name', 'city', 'owner', 'created_at', 'product_count']
        
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'created_at']
        
class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'store', 'category', 'created_at']