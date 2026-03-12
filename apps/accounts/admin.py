from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'camp', 'is_suspended', 'date_joined']
    list_filter = ['role', 'is_suspended', 'camp']
    search_fields = ['email', 'name', 'username']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('CampLearn', {
            'fields': ('name', 'phone', 'role', 'camp', 'is_suspended'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CampLearn', {
            'fields': ('name', 'email', 'phone', 'role', 'camp'),
        }),
    )
