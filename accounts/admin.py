from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'id_number', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Kenyan Details', {'fields': ('id_number', 'phone_number', 'physical_address')}),
    )

admin.site.register(User, CustomUserAdmin)