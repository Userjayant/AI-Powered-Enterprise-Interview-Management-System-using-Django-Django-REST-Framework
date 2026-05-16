"""accounts/admin.py"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'get_full_name', 'role', 'department', 'is_verified', 'date_joined']
    list_filter = ['role', 'department', 'is_verified', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('role', 'profile_image', 'phone_number', 'department', 'is_verified', 'bio', 'linkedin_url')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile Info', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'phone_number', 'department')
        }),
    )
