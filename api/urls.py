from rest_framework_nested import routers
from django.urls import path, include
from services.views import ServiceViewSet, ReviewViewSet, CategoryViewSet
from orders.views import OrderViewSet, NotificatinViewSet

router = routers.DefaultRouter()
router.register('services', ServiceViewSet, basename='services')
router.register('categories', CategoryViewSet, basename='categories')
# router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')
router.register('notifications', NotificatinViewSet, basename='notifications')


service_router = routers.NestedDefaultRouter(router, 'services', lookup = 'service')
service_router.register('reviews', ReviewViewSet, basename='service-review')







urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] + router.urls + service_router.urls
