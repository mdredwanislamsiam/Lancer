from django.contrib import admin
from services.models import Service, Review, Category, ServiceImage


admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ServiceImage)
