from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Category(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Service(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    service_requirements = models.TextField()
    delivery_time = models.DurationField()
    
    def __str__(self):
        return self.title
    
    
class Review(models.Model): 
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reviewed by {self.user.username} on {self.service.title}"