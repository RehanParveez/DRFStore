from django.shortcuts import render
from rest_framework import viewsets
from stores.models import Store, Category, Product
from stores.serializers import StoreSerializers, CategorySerializers, ProductsSerializers
from rest_framework.permissions import IsAuthenticated
from stores.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from stores.permissions import IsStoreOwnerOrReadOnly

# Create your views here.

class StoresViewset(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # fields to filter
    search_fields = ['name']
    ordering_fields = ['created_at']
    filterset_fields = ['city', 'owner', 'created_at']
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # fields to filter
    search_fields = ['name']
    ordering_fields = ['created_at']
    filterset_fields = ['name', 'created_at']
    
class ProductsViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializers
    permission_classes = [IsAuthenticated, IsStoreOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # fields to filter
    search_fields = ['name']
    ordering_fields = ['created_at']
    filterset_fields = ['name', 'price', 'store', 'category', 'created_at']