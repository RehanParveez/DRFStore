from rest_framework import serializers
from accounts.models import User

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'phone', 'dob', 'created_at']
        
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            phone=validated_data.get('phone'),
            dob=validated_data.get('dob'),
            created_at=validated_data.get('created_at'),  
        )
        return user