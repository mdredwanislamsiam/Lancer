from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
    SELLER = 'Seller'
    BUYER = 'Buyer'
    ROLE_CHOICES = (
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'), 
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    bio = models.TextField(null = True, blank=True)
    
    def __str__(self):
        return self.username
    

