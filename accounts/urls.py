from accounts.views import UsersViewset
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'Users', UsersViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('tokenobtainpair/', TokenObtainPairView.as_view()),
    path('tokenrefresh/', TokenRefreshView.as_view()),
]