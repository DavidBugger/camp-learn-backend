import uuid
from django.conf import settings
from django.db import models


class Badge(models.Model):
    """Achievement badge that can be earned by learners."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_url = models.URLField(blank=True)
    criteria = models.TextField(
        blank=True,
        help_text='Description of how to earn this badge',
    )
    points_required = models.PositiveIntegerField(
        default=0, help_text='Points threshold to auto-award'
    )
    lessons_required = models.PositiveIntegerField(
        default=0, help_text='Lessons completed threshold to auto-award'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['points_required']

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Badge awarded to a user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='badges',
    )
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='awards'
    )
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.user} — {self.badge.name}"


class PointTransaction(models.Model):
    """Points earned by a user for learning activities."""

    class Reason(models.TextChoices):
        LESSON_COMPLETE = 'lesson_complete', 'Lesson Completed'
        QUIZ_PASS = 'quiz_pass', 'Quiz Passed'
        QUIZ_PERFECT = 'quiz_perfect', 'Perfect Quiz Score'
        STREAK = 'streak', 'Learning Streak'
        BADGE = 'badge', 'Badge Earned'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='point_transactions',
    )
    points = models.IntegerField()
    reason = models.CharField(max_length=30, choices=Reason.choices)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}: +{self.points} ({self.reason})"
