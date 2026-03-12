from django.contrib import admin
from .models import Device, SyncLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_identifier', 'device_type', 'last_sync', 'created_at']
    list_filter = ['device_type']
    search_fields = ['device_identifier', 'user__name', 'user__email']


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'sync_status', 'records_uploaded', 'records_downloaded', 'synced_at']
    list_filter = ['sync_status']
