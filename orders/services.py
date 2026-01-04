from orders.models import Order, Notification
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrderServices: 
    
    @staticmethod
    def cancel_order(order, user): 
        with transaction.atomic(): 
            if user != order.buyer and user  != order.service.seller and not user.is_staff: 
                raise PermissionDenied({
                    'detail': 'You are not allowed to cancel this order'
                })
            
            if order.status in [Order.ACTIVE, Order.PAID]: 
                raise ValidationError({
                    'detail': 'This order cannot be canceled at this moment. Please contact admin for other ways.'
                })
            
            order.status = Order.CANCELED
            order.save()
            message_for_seller = f"Order {order.id} has been canceled"
            message_for_buyer = f"Your order for {order.service.title} has been canceled"
            OrderServices.create_notification(
                user=order.buyer, message=message_for_buyer)
            OrderServices.create_notification(
                user=order.service.seller, message=message_for_seller)
            return order
    
    @staticmethod
    def create_notification(user, message): 
        return Notification.objects.create(user = user, message = message)