from django.db import models
from users.models import User
from services.models import Service
from uuid import uuid4


class Order(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    NOT_PAID = 'Not paid'
    PAID = 'Paid'
    ACTIVE = 'Active'
    CANCELED = 'Canceled'
    STATUS_CHOICES = (
        (NOT_PAID, 'Not paid'),
        (PAID, 'Paid'),
        (ACTIVE, 'Active'),
        (CANCELED, 'Canceled'),
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_PAID)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.buyer.username} - {self.status}"

    

class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification For {self.user}"
    