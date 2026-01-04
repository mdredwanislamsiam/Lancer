from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from orders.serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer, NotificationSerializer, UpdateNotificationSerializer
from orders.models import Order, Notification
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.services import OrderServices
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
    
    
class OrderViewSet(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    @swagger_auto_schema(
        operation_summary="Cancel order",
        request_body=EmptySerializer,
        responses={200: openapi.Response(
            description="Order canceled",
            examples={"application/json": {"status": "Order Canceled"}}
        )}
    )
    @action(detail = True, methods=['post'])
    def cancel(self, request, pk = None): 
        order = self.get_object()
        OrderServices.cancel_order(order=order, user = request.user)
        return Response({
            'status': 'Order Canceled'
        })


    @swagger_auto_schema(
        operation_summary="Update order status",
        request_body=UpdateOrderSerializer,
        responses={200: openapi.Response(
            description="Order status updated",
            examples={
                "application/json": {"status": "Order status updated to PAID"}}
        )}
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk = None): 
        order = self.get_object()
        old_status = order.status
        
        serializer = UpdateOrderSerializer(order, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if old_status != Order.PAID and order.status == Order.PAID: 
            message_for_seller = f"Order {order.id} has been paid."
            message_for_buyer = f"Your order for {order.service.title} has been marked as PAID"
            OrderServices.create_notification(
                user=order.buyer, message=message_for_buyer)
            OrderServices.create_notification(
                user=order.service.seller, message=message_for_seller)
        
        return Response({'status': f'Order status updated to {request.data.get('status')}'})
    
    
    def get_serializer_class(self):
        if self.action == 'cancel': 
            return EmptySerializer
        if self.request.method == "POST": 
            return CreateOrderSerializer
        if self.action == 'update_status': 
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        if self.request.user.is_staff : 
            return Order.objects.select_related('service').all()
        return Order.objects.select_related('service').filter(buyer = self.request.user)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']: 
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    
    
    @swagger_auto_schema(
        operation_summary="List orders",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create order",
        request_body=CreateOrderSerializer,
        responses={201: OrderSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve order",
        responses={200: OrderSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary= "Partial Update Order",
        request_body= UpdateOrderSerializer,
        responses={200: OrderSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete order",
        operation_description="Only admin can delete an order",
        responses={
            204: "No Content",
            403: "Forbidden"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    
class NotificatinViewSet(ModelViewSet): 
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List notifications",
        responses={200: NotificationSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve notification",
        responses={200: NotificationSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mark notification as read",
        request_body=UpdateNotificationSerializer,
        responses={200: NotificationSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete notification",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'partial_update': 
            return UpdateNotificationSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False): 
            return Notification.objects.none()
        return Notification.objects.select_related('user').filter(user = self.request.user).order_by("-created_at")