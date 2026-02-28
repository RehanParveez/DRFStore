from stores.views import StoresViewset, CategoryViewset, ProductsViewset
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from stores.views import StoresTokenObtainPairView, StoresTokenRefreshView

router = DefaultRouter()
router.register(r'Stores', StoresViewset, basename='stores')
router.register(r'Categories', CategoryViewset, basename='categories')
router.register(r'Products', ProductsViewset, basename='products')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/tokenobtainpair/', StoresTokenObtainPairView.as_view()),
    path('api/v1/tokenrefresh/', StoresTokenRefreshView.as_view()),
]