from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from orders.serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer, NotificationSerializer
from orders.models import Order, Notification
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from orders.services import OrderServices
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import User
from services.permissions import IsBuyerOrReadOnly
from rest_framework.views import APIView
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status
from users.models import IncomeOrCostPerMonth
from datetime import date

    
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
            order.service.count += 1 
            order.service.save()
            title = "Payment Notification"
            message_for_seller = f"Order {order.id} has been paid."
            message_for_buyer = f"Your order for {order.service.title} has been marked as PAID"
            OrderServices.create_notification(
                user=order.buyer, message=message_for_buyer, title=title)
            OrderServices.create_notification(
                user=order.service.seller, message=message_for_seller, title=title)
        
        return Response({'status': f"Order status updated to {request.data.get('status')}"})
    
    
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
            return Order.objects.none()
        queryset = Order.objects.select_related('service', 'service__seller', 'buyer', 'service__category',).prefetch_related('service__images')
        if self.request.user.is_staff:
            return queryset.order_by("-created_at")
        if self.request.user.role == User.BUYER:
            return queryset.filter(buyer=self.request.user).order_by("-created_at")
        return queryset.filter(service__seller=self.request.user).order_by("-created_at")
        
    def get_serializer_context(self):
        return {'user': self.request.user}
    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy', 'partial_update']: 
            return [permissions.IsAdminUser()]
        if self.action == 'cancel': 
            return [permissions.IsAuthenticated()]
        if self.action == 'create': 
            return [IsBuyerOrReadOnly()]
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
    serializer_class = NotificationSerializer
    
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
        operation_summary="Delete notification",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False): 
            return Notification.objects.none()
        return Notification.objects.select_related('user').filter(user = self.request.user).order_by("-created_at")
    

class UpdateNotification(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, notification_id): 
        notification = Notification.objects.get(id = notification_id)
        notification.is_read = True; 
        notification.save(); 
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class CanOrderService(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, service_id):
        user = request.user

        active_order_exists = Order.objects.filter(
            buyer=user,
            service_id=service_id
        ).exclude(
            status__in=[Order.DELIVERED, Order.CANCELED]
        ).exists()

        return Response({
            "can_order": not active_order_exists
        })
    
    
    
@api_view(['POST'])
def initiate_payment(request):

    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("orderId")

    ssl_settings = {'store_id': 'phima6975dc6e2e54d',
                    'store_pass': 'phima6975dc6e2e54d@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(ssl_settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"tr_{order_id}"
    post_body['success_url'] = f"{settings.BACKEND_URL}/api/payment/success"
    post_body['fail_url'] = f"{settings.BACKEND_URL}/api/payment/fail"
    post_body['cancel_url'] = f"{settings.BACKEND_URL}/api/payment/cancel"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['product_name'] = "Freelancing Platform"
    post_body['product_category'] = "General Category"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)  # API response

    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response.get("GatewayPageURL")})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def payment_success(request):
    order_id = request.data.get("tran_id").split('_')[1]
    order = Order.objects.get(id=order_id)
    
    today = date.today()
    month_date = date(today.year, today.month, 1)
    buyer_wallet, _ = IncomeOrCostPerMonth.objects.get_or_create(user = order.buyer, month_and_year = month_date, defaults={'amount': 0})
    seller_wallet, _ = IncomeOrCostPerMonth.objects.get_or_create(user=order.service.seller, month_and_year= month_date, defaults={'amount': 0})
    order.buyer.wallet += order.total_price
    order.service.seller.wallet += order.total_price
    order.buyer.save()
    order.service.seller.save()

    
    buyer_wallet.amount += order.total_price
    buyer_wallet.save()
    seller_wallet.amount += order.total_price
    seller_wallet.save()
    
    
    order.status = "Paid"
    order.save()
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")


@api_view(["POST"])
def payment_cancel(request):
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")


@api_view(["POST"])
def payment_fail(request):
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")


class HasOrderedProduct(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, service_id):
        user = request.user
        has_ordered = Order.objects.filter(
            buyer=user, service_id=service_id, status = Order.DELIVERED).exists()
        return Response({"has_ordered": has_ordered})


class GetAdminOrders(APIView):
    permission_classes = [permissions.IsAdminUser]

