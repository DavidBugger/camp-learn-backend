from rest_framework import serializers
from .models import Device, SyncLog


class DeviceRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id', 'device_identifier', 'device_type',
            'device_name', 'last_sync', 'created_at',
        ]
        read_only_fields = ['id', 'last_sync', 'created_at']


class SyncUploadSerializer(serializers.Serializer):
    """Serializer for uploading offline activity."""
    device_identifier = serializers.CharField()
    lesson_completions = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text='List of {lesson_id, completed_at}',
    )
    quiz_submissions = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text='List of {quiz_id, answers, submission_uid}',
    )


class SyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncLog
        fields = [
            'id', 'device', 'sync_status',
            'records_uploaded', 'records_downloaded',
            'error_message', 'synced_at',
        ]


class ContentUpdateSerializer(serializers.Serializer):
    """Response for content updates since last sync."""
    new_courses = serializers.ListField(child=serializers.DictField())
    new_lessons = serializers.ListField(child=serializers.DictField())
    updated_lessons = serializers.ListField(child=serializers.DictField())
