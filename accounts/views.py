from django.shortcuts import render
from rest_framework import viewsets
from accounts.models import User
from accounts.serializers import UsersSerializers
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

# Create your views here.

class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # fields to filter
    search_fields = ['email']
    ordering_fields = ['created_at']
    filterset_fields = ['email', 'created_at']
    
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]