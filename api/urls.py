from rest_framework_nested import routers
from django.urls import path, include
from services.views import ServiceViewSet, ReviewViewSet, CategoryViewSet, ServiceImageViewSet, MyServices, HasReviewed, GetCategoricalServices, GetReviews
from orders.views import OrderViewSet, NotificatinViewSet, CanOrderService, initiate_payment, payment_fail, payment_success, payment_cancel, UpdateNotification, HasOrderedProduct
from users.views import PublicUserView, IncomeOrCostPerMonthViewSet, OtherInfo



router = routers.DefaultRouter()

router.register('services', ServiceViewSet, basename='services')
router.register('categories', CategoryViewSet, basename='categories')
# router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')
router.register('notifications', NotificatinViewSet, basename='notifications')


service_router = routers.NestedDefaultRouter(router, 'services', lookup = 'service')
service_router.register('reviews', ReviewViewSet, basename='service-review')
service_router.register('images', ServiceImageViewSet, basename='service-image')






urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('orders/can_order/<int:service_id>', CanOrderService.as_view(), name='can-order'),
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path('payment/success', payment_success, name="payment-success"),
    path('payment/fail', payment_fail, name="payment-fail"),
    path('payment/cancel', payment_cancel, name="payment-cancel"),
    path('notifications/mark/<int:notification_id>', UpdateNotification.as_view(), name="update-notification"), 
    path('services/my/', MyServices.as_view(), name="my-services"), 
    path('orders/has-ordered/<int:service_id>',
         HasOrderedProduct.as_view(), name='has-ordered-service'),
    path('services/<int:service_id>/reviews/has-reviewed/',
         HasReviewed.as_view(), name='has-reviewed'),
    path('categories/five_services/<int:category_id>', GetCategoricalServices.as_view(), name="categoy-services"),
    path('reviews', GetReviews.as_view(), name='reviews' ), 
    path('other_info', OtherInfo.as_view(), name='otherInfo' ), 
    path('income_data', IncomeOrCostPerMonthViewSet.as_view(), name='income-data'), 
    path('users/<int:id>', PublicUserView.as_view(), name= 'each-user'), 
] + router.urls + service_router.urls
