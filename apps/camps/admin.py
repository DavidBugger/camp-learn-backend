from django.contrib import admin
from .models import Camp


@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'state', 'country', 'created_at']
    search_fields = ['name', 'location', 'state']
    list_filter = ['state', 'country']
