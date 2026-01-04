from django_filters.rest_framework import FilterSet 
from services.models import Service


class ServiceFilter(FilterSet): 
    class Meta: 
        model = Service 
        fields = {
            'price': ['gte', 'lte'],
            'category_id': ['exact'], 
        }