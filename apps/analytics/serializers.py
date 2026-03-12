from rest_framework import serializers


class PlatformStatsSerializer(serializers.Serializer):
    """Aggregate statistics for the entire platform."""
    total_learners = serializers.IntegerField()
    total_facilitators = serializers.IntegerField()
    total_camps = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_learning_hours = serializers.FloatField()
    overall_completion_rate = serializers.FloatField()


class CampStatsSerializer(serializers.Serializer):
    """Aggregate statistics for a specific camp."""
    camp_id = serializers.UUIDField()
    camp_name = serializers.CharField()
    total_learners = serializers.IntegerField()
    active_learners_30d = serializers.IntegerField()
    courses_completed = serializers.IntegerField()
    total_learning_hours = serializers.FloatField()


class CourseStatsSerializer(serializers.Serializer):
    """Aggregate statistics for a specific course."""
    course_id = serializers.UUIDField()
    course_title = serializers.CharField()
    total_enrolled = serializers.IntegerField()
    total_completed = serializers.IntegerField()
    average_quiz_score = serializers.FloatField()
