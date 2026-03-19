from rest_framework import serializers
from users.models import User, IncomeOrCostPerMonth
from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer, UserSerializer

        
class CustomUserCreateSerializer(UserCreateSerializer):
    image = serializers.ImageField()
    class Meta(UserCreateSerializer.Meta): 
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password',
                    'phone_number', 'address', 'image', 'bio', 'role']
      
    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = super().create(validated_data)
        if role:
            user.role = role
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        user.save()
        return user



class CustomUserSerializer(UserSerializer):
    image = serializers.ImageField()
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                   'phone_number', 'address', 'bio', 'image', 'role', 'wallet', 'is_staff']
        ref_name = 'CustomUser'
        read_only_fields = ['is_staff', 'wallet']

class SimpleUserSerializer(UserSerializer): 
    image = serializers.ImageField()
    class Meta(UserSerializer.Meta): 
        fields = ['id', 'username', 'image']
        ref_name = 'SimpleUser'


class IncomeOrCostPerMonthSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta: 
        model = IncomeOrCostPerMonth
        fields = ['id', 'user', 'amount', 'month_and_year']