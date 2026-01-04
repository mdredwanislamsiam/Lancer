from services.models import Service, Category, Review
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import timedelta



class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
        read_only_fields = ['username']



class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = ['id', 'name', 'description', 'service_count']
        
    service_count = serializers.IntegerField(read_only = True)
    
    
     
class ServiceSerializer(serializers.ModelSerializer):
    delivery_weeks = serializers.IntegerField(write_only =True)
    delivery_days = serializers.IntegerField(write_only = True)
    delivery_hours = serializers.IntegerField(write_only = True)
    
    delivery_time = serializers.SerializerMethodField(read_only = True)
    seller = SimpleUserSerializer(read_only = True)
    class Meta: 
        model = Service 
        fields = ['id', 'title', 'description', 'category', 'price', 'seller', 'service_requirements', 'delivery_weeks', 'delivery_days', 'delivery_hours', 'delivery_time']
    
    
    def create(self, validated_data):
        weeks = validated_data.pop('delivery_weeks', 0)
        days = validated_data.pop('delivery_days', 0)
        hours = validated_data.pop('delivery_hours', 0)
        if weeks or days or hours:
            validated_data['delivery_time'] = timedelta(weeks=weeks, days=days, hours=hours)
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        weeks = validated_data.pop('delivery_weeks', 0)
        days = validated_data.pop('delivery_days', 0)
        hours = validated_data.pop('delivery_hours', 0)
        if weeks or days or hours: 
            validated_data['delivery_time'] = timedelta(weeks=weeks, days=days, hours=hours)
        return super().update(instance, validated_data)
    
    def get_delivery_time(self, obj): 
        total_seconds = int(obj.delivery_time.total_seconds())
        weeks = total_seconds//(7*24*3600)
        days = (total_seconds%(7*24*3600))//(24*3600)
        hours = (total_seconds%(24*3600))//3600
        
        return f"{weeks:02d} weeks {days:02d} days {hours:02d} hours"
    


class ReviewSerializer(serializers.ModelSerializer): 
    user = SimpleUserSerializer(read_only = True)
    service = serializers.StringRelatedField()
    class Meta: 
        model = Review 
        fields = ['id', 'user', 'service', 'ratings', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['service']
        
    def create(self, validated_data):
        return Review.objects.create(service_id = self.context['service_pk'], **validated_data)


