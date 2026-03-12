from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content_type',
            'content_url', 'content_text', 'duration', 'order', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category',
            'created_at', 'updated_at', 'lesson_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lessons']


class LessonDownloadSerializer(serializers.ModelSerializer):
    """Minimal serializer for offline download."""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content_type', 'content_url', 'content_text', 'duration']
