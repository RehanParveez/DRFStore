from accounts.views import UsersViewset
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'Users', UsersViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]