from rest_framework import serializers
from .models import LessonProgress


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = [
            'id', 'user', 'lesson', 'lesson_title',
            'completed', 'completion_time', 'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']


class MarkLessonCompleteSerializer(serializers.Serializer):
    lesson_id = serializers.UUIDField()


class CourseProgressSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()
    course_title = serializers.CharField()
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    percentage = serializers.FloatField()


class LearningStatsSerializer(serializers.Serializer):
    total_lessons_completed = serializers.IntegerField()
    total_courses_started = serializers.IntegerField()
    total_quizzes_taken = serializers.IntegerField()
    total_learning_hours = serializers.FloatField()
