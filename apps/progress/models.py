import uuid
from django.conf import settings
from django.db import models


class LessonProgress(models.Model):
    """Tracks a learner's progress on a specific lesson."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
    )
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.CASCADE,
        related_name='progress_records',
    )
    completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name_plural = 'Lesson progress records'
        ordering = ['-updated_at']

    def __str__(self):
        status = 'Completed' if self.completed else 'In Progress'
        return f"{self.user} — {self.lesson.title}: {status}"
