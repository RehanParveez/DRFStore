from django.shortcuts import render
from rest_framework import viewsets
from stores.models import Store, Category, Product
from stores.serializers import StoreSerializers, CategorySerializers, ProductsSerializers
# Create your views here.

class StoresViewset(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    
class ProductsViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializers