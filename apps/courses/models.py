import uuid
from django.db import models


class Course(models.Model):
    """Educational course available on the platform."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Individual lesson within a course."""

    class ContentType(models.TextChoices):
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        TEXT = 'text', 'Text'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content_type = models.CharField(
        max_length=10, choices=ContentType.choices, default=ContentType.TEXT
    )
    content_url = models.FileField(upload_to='lessons/', blank=True)
    content_text = models.TextField(blank=True, help_text='For text-based lessons')
    duration = models.PositiveIntegerField(
        default=0, help_text='Duration in minutes'
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.title} — {self.title}"
