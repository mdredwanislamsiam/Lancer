from rest_framework import serializers
from users.models import User
from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer, UserSerializer

        
class CustomUserCreateSerializer(UserCreateSerializer): 
    class Meta(UserCreateSerializer.Meta): 
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password',
                    'phone_number', 'address', 'bio', 'role']
      
      
    def create(self, validated_data):
        role = validated_data['role']
        user = super().create(validated_data)
        group, _ = Group.objects.get_or_create(name = role)
        user.groups.add(group)
        return user
    


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                   'phone_number', 'address', 'bio', 'role']
        ref_name = 'CustomUser'
