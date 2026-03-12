from django.contrib import admin
from .models import Badge, UserBadge, PointTransaction


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'lessons_required', 'created_at']
    search_fields = ['name']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    list_filter = ['badge']


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'reason', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__name', 'user__email']
