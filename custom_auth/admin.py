from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'role', 'is_active')
    search_fields = ('role', 'email')
    list_filter = ('role',)
    ordering = ('id',)



