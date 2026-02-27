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
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from stores.pagination import ProductPagination

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
    
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def get_queryset(self):
        users = self.request.user
        if users.is_staff:
            return Store.objects.all()
        return Store.objects.filter(owner=users)
    
    # getting all the products of a store
    @action(detail=True, methods=['get'])
    def products_store(self, request, pk=None):
        store = self.get_object()
        products = store.products.all()
        serializer = ProductsSerializers(products, many=True)
        return Response(serializer.data)
        
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
    
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def get_queryset(self):
        users = self.request.user
        if users.is_staff:
            return Category.objects.all()
        return Category.objects.filter(store__owner = users)
    
    # getting the products inside the category
    @action(detail=True, methods=['get'])
    def products_category(self, request, pk=None):
        category = self.get_object()
        products = category.products.all()
        serializer = ProductsSerializers(products, many=True)
        return Response(serializer.data)
    
    # counting product in the category
    @action(detail=True, methods=['get'])
    def product_count(self, request, pk=None):
        category = self.get_object()
        count = category.products.count()
        return Response({'total products': count})
    
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
    
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    pagination_class =ProductPagination
    
    def get_queryset(self):
        users = self.request.user
        if users.is_staff:
            return Product.objects.all()
        return Product.objects.filter(store__owner=users)
    
    # the low stock products
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = self.get_queryset().filter(quantity__lt=5)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    # the most expensive products
    @action(detail=False, methods=['get'])
    def expensive(self, request):
        products = self.get_queryset().order_by('-price')[:7]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)