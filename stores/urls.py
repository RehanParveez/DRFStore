from stores.views import StoresViewset, CategoryViewset, ProductsViewset
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'Stores', StoresViewset, basename='stores')
router.register(r'Categories', CategoryViewset, basename='categories')
router.register(r'Products', ProductsViewset, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]