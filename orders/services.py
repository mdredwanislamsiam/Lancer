from orders.models import Order, Notification
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrderServices: 
    
    @staticmethod
    def cancel_order(order, user): 
        with transaction.atomic(): 
            if user.is_staff: 
                order.status = Order.CANCELED
                message_for_seller = f"Order {order.id} has been canceled"
                message_for_buyer = f"Your order for {order.service.title} has been canceled"
                OrderServices.create_notification(
                    user=order.buyer, message=message_for_buyer)
                OrderServices.create_notification(
                    user=order.service.seller, message=message_for_seller)
                order.save()
            if order.buyer != user: 
                raise PermissionDenied({
                    'detail': 'You can only cancel your own orders'
                })
            if (order.status == Order.ACTIVE or order.status == Order.PAID): 
                raise ValidationError({
                    'detail': 'This order can not be canceled at this moment. Please contact the Admin for further information.'
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