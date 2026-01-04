from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin): 
    model = User 
    list_display = ('username', 'email', 'first_name', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, 
            {
                'fields': ('username', 'email', 'password')
            }
        ), 
        ('Personal Info',
            {
                'fields': ('first_name', 'last_name', 'role', 'address', 'phone_number')
            }
        ), 
        ('Permissions', 
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ), 
        ('Important Dates',
            {
                'fields': ('last_login', 'date_joined')
            }
        )
    )
    add_fieldsets = (
        (None,
            {
                'classes': ('wide', ), 
                'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'address', 'is_staff', 'is_active')
            }
        ), 
    )
    search_fields = ('email', 'phone_number', 'username' )
    ordering = ('email', )