from django.shortcuts import render
from rest_framework import viewsets
from accounts.models import User
from accounts.serializers import UsersSerializers
# Create your views here.

class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers