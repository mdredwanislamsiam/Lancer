from django.contrib import admin
from orders.models import Order, Notification


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): 
    list_display = ['id', 'buyer', 'status']
    
    
admin.site.register(Notification)