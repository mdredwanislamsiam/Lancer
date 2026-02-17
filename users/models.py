from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

    
    

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
    image = CloudinaryField("image", null = True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    
    def __str__(self):
        return self.username


class IncomeOrCostPerMonth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet_history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month_and_year = models.DateField()
