from rest_framework import serializers
from orders.models import Order, Notification
from services.models import Service
from orders.services import OrderServices




class SimpleServiceSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Service
        fields = ['id', 'title', 'price']
        
        

class OrderSerializer(serializers.ModelSerializer):
    service = SimpleServiceSerializer()
    class Meta: 
        model = Order
        fields = ['id', 'buyer', 'status', 'service', 'total_price', 'created_at', 'updated_at']
        
        

class CreateOrderSerializer(serializers.Serializer): 
    service_id = serializers.IntegerField()
    
    def validate_service_id(self, service_id): 
        if not Service.objects.filter(pk = service_id).exists(): 
            raise serializers.ValidationError({
                'detail': 'No Such Service Found'
            })
        return service_id
    
    def create(self, validated_data): 
        user_id = self.context['user_id']
        service_id = validated_data['service_id']
        
        service = Service.objects.get(pk = service_id)
        total_price = service.price
        order = Order.objects.create(buyer_id = user_id, total_price= total_price, service= service)
        
        message_for_seller = f"A new order was is made by {order.buyer} for the {service.title} service. Wait for the payment." 
        message_for_buyer = f"To confirm Your order for {service.title} Please Proceed with the payment. Your bill is ${total_price}."
        OrderServices.create_notification(user = order.buyer, message= message_for_buyer)
        OrderServices.create_notification(user= service.seller, message= message_for_seller)
        
        return order

        

class UpdateOrderSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Order
        fields = ['status']
    

class EmptySerializer(serializers.Serializer): 
    pass



#      Serializer For Notifications


class NotificationSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        
    
    
class UpdateNotificationSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Notification
        fields = ['is_read']