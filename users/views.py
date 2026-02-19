from .models import User, IncomeOrCostPerMonth
from .serializers import CustomUserSerializer, IncomeOrCostPerMonthSerializer, SimpleUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from services.models import Service, Review
from orders.models import Order
from rest_framework.response import Response
from services.serializers import ServiceSerializer
from orders.serializers import OrderSerializer


class PublicUserView(APIView):
    def get(self, request, id): 
        user = User.objects.get(id = id)
        if(request.user.is_authenticated): 
            return Response ({'user': CustomUserSerializer(user).data})
        return Response({'user': SimpleUserSerializer(user).data})
    


class IncomeOrCostPerMonthViewSet(APIView):
    def get(self, request): 
        user = request.user
        income_data = IncomeOrCostPerMonth.objects.prefetch_related(
            "user").filter(user = user ); 
        return Response({"income_data": IncomeOrCostPerMonthSerializer(income_data, many = True).data})
    


class OtherInfo(APIView):
    def get(self, request):
        user = self.request.user
        service_query = Service.objects.select_related(
            'category', 'seller').prefetch_related('images')
        order_query = Order.objects.select_related(
            'service', 'service__seller', 'buyer', 'service__category').prefetch_related('service__images').order_by('-created_at')
        numOrder = order_query.count(); 
        
        if (user.is_staff):
            
            delivered_orders = order_query.filter(status=Order.DELIVERED)
            unpaid_orders = order_query.filter(status=Order.NOT_PAID)
            paid_orders = order_query.filter(status=Order.PAID)
            canceled_orders = order_query.filter(status=Order.CANCELED)
            active_orders = order_query.filter(status=Order.ACTIVE)
            total_orders = order_query.all()

            return Response({
                "delivered_orders": OrderSerializer(delivered_orders, many=True).data,
                "active_orders": OrderSerializer(active_orders, many=True).data,
                "paid_orders": OrderSerializer(paid_orders, many=True).data,
                "unpaid_orders": OrderSerializer(unpaid_orders, many=True).data,
                "canceled_orders": OrderSerializer(canceled_orders, many=True).data,
                "total_orders": OrderSerializer(total_orders, many=True).data,
                "numOrder": numOrder,
            })
        
        total_services = service_query.filter(orders__buyer=user)
        total_orders = order_query.filter(buyer=user)
        total_clients = User.objects.filter(
            role=User.SELLER, services__orders__buyer=user).distinct()
        if (user.role == User.SELLER):
            total_services = service_query.filter(seller=user)
            total_orders = order_query.filter(service__seller=user)
            total_clients = User.objects.filter(
                role=User.BUYER, orders__service__seller=user).distinct()
        

     
        delivered_orders = total_orders.filter(status=Order.DELIVERED)
        active_orders = total_orders.filter(status=Order.ACTIVE)
        unpaid_orders = total_orders.filter(status=Order.NOT_PAID)
        paid_orders = total_orders.filter(status=Order.PAID)
        canceled_orders = total_orders.filter(status=Order.CANCELED)

        return Response({"total_services": ServiceSerializer(total_services, many=True).data,
                         "total_orders": OrderSerializer(total_orders, many=True).data, 
                         "paid_orders": OrderSerializer(paid_orders, many=True).data,
                         "unpaid_orders": OrderSerializer(unpaid_orders, many=True).data,
                         "canceled_orders": OrderSerializer(canceled_orders, many=True).data,
                         "delivered_orders": OrderSerializer(delivered_orders, many=True).data, 
                         "active_orders": OrderSerializer(active_orders, many=True).data, 
                         "total_clients": CustomUserSerializer(total_clients, many=True).data, 
                         "numOrder": numOrder, 
                        })
