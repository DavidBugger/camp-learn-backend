from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'content_type', 'duration', 'order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_filter = ['category']
    # inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content_type', 'duration', 'order']
    list_filter = ['content_type', 'course']
    search_fields = ['title']
