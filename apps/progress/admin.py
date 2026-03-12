from django.contrib import admin
from .models import LessonProgress


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'completion_time', 'created_at']
    list_filter = ['completed', 'lesson__course']
    search_fields = ['user__name', 'user__email', 'lesson__title']
