from accounts.views import UsersViewset
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts.views import AccountsTokenObtainPairView, AccountsTokenRefreshView

router = DefaultRouter()
router.register(r'Users', UsersViewset, basename='users')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/tokenobtainpair/', AccountsTokenObtainPairView.as_view()),
    path('api/v1/tokenrefresh/', AccountsTokenRefreshView.as_view()),
]