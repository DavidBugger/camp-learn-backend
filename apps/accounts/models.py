import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for CampLearn platform."""

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        FACILITATOR = 'facilitator', 'Facilitator'
        ADMIN = 'admin', 'Camp Admin'
        SYSTEM_ADMIN = 'system_admin', 'System Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    camp = models.ForeignKey(
        'camps.Camp',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )
    is_suspended = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name or self.username} ({self.role})"
