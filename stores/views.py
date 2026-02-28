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
from django.db.models import Sum, F, Count
from django.db import connection
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from stores.throttles import Login, Refresh

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
        queryset1 = Store.objects.select_related('owner').prefetch_related('products')
        if users.is_staff:
            return queryset1
        return queryset1.filter(owner=users)
    
    # getting all the products of a store   (updated)
    @action(detail=True, methods=['get'])
    def products_store(self, request, pk=None):
        store = self.get_object()
        serializer = ProductsSerializers(store.products.all(), many=True)
        return Response(serializer.data)
    
    # total inventory value per store
    @action(detail=True, methods=['get'])
    def inventory(self, request, pk=None):
        store = self.get_object()
        total = store.products.aggregate(total_inventory=Sum(F('price') * F('quantity')))
        return Response(total)
    
    # stores with count of product
    @action(detail=False, methods=['get'])
    def strpro_count(self, request):
        stores = self.get_queryset().annotate(product_count=Count('products'))
        serializer = self.get_serializer(stores, many=True)
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
        queryset1 = Category.objects.prefetch_related('products__store', 'products__category')
        if users.is_staff:
            return queryset1
        return queryset1.filter(products__store__owner = users)
    
    # getting the products inside the category
    @action(detail=True, methods=['get'])
    def products_category(self, request, pk=None):
        category = self.get_object()
        serializer = ProductsSerializers(category.products.all(), many=True)
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
        queryset1 = Product.objects.select_related('store', 'category', 'store__owner')
        if users.is_staff:
            return queryset1
        return queryset1.filter(store__owner = users)
    
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
    
    # showing products with store name and owner email
    @action(detail=False, methods=['get'])
    def info(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
               SELECT
                     stores_product.id,
                     stores_product.name,
                     stores_product.price,
                     stores_product.quantity,
                     stores_store.name AS store_name,
                     accounts_user.email AS owner_email
                FROM stores_product
                INNER JOIN stores_store ON stores_product.store_id = stores_store.id
                INNER JOIN accounts_user ON stores_store.owner_id = accounts_user.id
            """)
            rows = cursor.fetchall()
        return Response(rows)

class StoresTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [Login]

class StoresTokenRefreshView(TokenRefreshView):
    throttle_classes = [Refresh]