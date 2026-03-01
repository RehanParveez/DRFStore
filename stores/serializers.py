from rest_framework import serializers
from stores.models import Store, Category, Product
from accounts.serializers import UsersSerializers

class StoreSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'city', 'is_active']

class ProductSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'store', 'category']
    
    def validate_price(self, value):
        print("VALIDATE PRICE CALLED", value)
        if value <= 0:
            raise serializers.ValidationError('the price should be greater than zero')
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('the quantity cant be zero')
        return value

    def validate(self, data):
        store = data.get('store')
        category = data.get('category')
        name = data.get('name')
        user = self.context['request'].user

        if not store.is_active:
            raise serializers.ValidationError('store is not active')

        if store.owner != user:
            raise serializers.ValidationError('the store owner can only add the product')

        if category.store != store:
            raise serializers.ValidationError('the category should be related to the store')

        if Product.objects.filter(store=store, name=name).exists():
            raise serializers.ValidationError('the product already exists in this store')
        return data

class StoreSerializers(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    products = ProductSerializer1(many=True, read_only=True)
    owner = UsersSerializers(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'name', 'city', 'owner', 'created_at', 'is_active', 'product_count', 'products']
        
class CategorySerializers(serializers.ModelSerializer):
    store = StoreSerializer1(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'store']
        
class CategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'store']

    def validate(self, data):
        store = data.get('store')
        user = self.context['request'].user
        
        if store.owner != user:
            raise serializers.ValidationError("not owner of the store")
        return data
        
class ProductsSerializers(serializers.ModelSerializer):
    store = StoreSerializer1(read_only=True)
    category = CategorySerializers(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'store', 'category', 'created_at']