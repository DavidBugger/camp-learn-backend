import uuid
from django.conf import settings
from django.db import models


class Device(models.Model):
    """Registered device for a user."""

    class DeviceType(models.TextChoices):
        ANDROID = 'android', 'Android'
        IOS = 'ios', 'iOS'
        WEB = 'web', 'Web Browser'
        HUB = 'hub', 'Learning Hub'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='devices',
    )
    device_identifier = models.CharField(
        max_length=255, unique=True,
        help_text='Unique hardware or browser fingerprint',
    )
    device_type = models.CharField(
        max_length=10, choices=DeviceType.choices, default=DeviceType.ANDROID
    )
    device_name = models.CharField(max_length=255, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_sync']

    def __str__(self):
        return f"{self.user} — {self.device_identifier}"


class SyncLog(models.Model):
    """Log of sync operations between device and server."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='sync_logs'
    )
    sync_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    records_uploaded = models.PositiveIntegerField(default=0)
    records_downloaded = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-synced_at']

    def __str__(self):
        return f"{self.device}: {self.sync_status} @ {self.synced_at}"
