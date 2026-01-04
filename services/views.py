from drf_yasg.utils import swagger_auto_schema
from services.models import Service, Review, Category
from rest_framework.viewsets import ModelViewSet 
from services.serializers import ServiceSerializer, ReviewSerializer, CategorySerializer
from django.db.models import Count
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from services.filters import ServiceFilter
from rest_framework.pagination import PageNumberPagination




class ServiceViewSet(ModelViewSet): 
    queryset = Service.objects.select_related('category').select_related('seller').all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title']
    ordering_fields = ['price']
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_summary="List services",
        responses={200: ServiceSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create service",
        operation_description="Authenticated user creates a service. Seller is auto assigned.",
        request_body=ServiceSerializer,
        responses={201: ServiceSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve service",
        responses={200: ServiceSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update service",
        request_body=ServiceSerializer,
        responses={200: ServiceSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update service",
        request_body=ServiceSerializer,
        responses={200: ServiceSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete service",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(seller = self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(seller = self.request.user)
    
    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(service_count=Count('services')).all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List categories",
        operation_description="Retrieve all categories with service count",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve category",
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete category",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    
    
class ReviewViewSet(ModelViewSet): 
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    @swagger_auto_schema(
        operation_summary="List service reviews",
        responses={200: ReviewSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create service review",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve review",
        responses={200: ReviewSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update review",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update review",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete review",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Review.objects.filter(service_id = self.kwargs.get('service_pk'))
    
    def get_serializer_context(self):
        return {'service_pk': self.kwargs['service_pk']}
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

