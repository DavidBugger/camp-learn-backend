from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from apps.accounts.permissions import IsAdmin
from apps.camps.models import Camp
from apps.courses.models import Course
from apps.progress.models import LessonProgress
from apps.quizzes.models import QuizSubmission
from .serializers import (
    PlatformStatsSerializer,
    CampStatsSerializer,
    CourseStatsSerializer,
)

User = get_user_model()


class PlatformStatsView(APIView):
    """GET /analytics/platform — Overall platform statistics."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        total_learners = User.objects.filter(role='student').count()
        total_facilitators = User.objects.filter(role='facilitator').count()
        total_camps = Camp.objects.count()
        total_courses = Course.objects.count()

        # Learning hours estimated from completed lessons
        total_minutes = (
            LessonProgress.objects.filter(completed=True)
            .aggregate(total=Sum('lesson__duration'))['total']
        ) or 0

        # Completion rate (completed lessons / total lesson starts)
        starts = LessonProgress.objects.count()
        completes = LessonProgress.objects.filter(completed=True).count()
        rate = (completes / starts * 100) if starts > 0 else 0.0

        data = {
            'total_learners': total_learners,
            'total_facilitators': total_facilitators,
            'total_camps': total_camps,
            'total_courses': total_courses,
            'total_learning_hours': round(total_minutes / 60, 1),
            'overall_completion_rate': round(rate, 1),
        }
        serializer = PlatformStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CampStatsView(APIView):
    """GET /analytics/camp/{camp_id} — Advanced camp analytics."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request, camp_id):
        try:
            camp = Camp.objects.get(pk=camp_id)
        except Camp.DoesNotExist:
            raise NotFound('Camp not found')

        learners = User.objects.filter(camp=camp, role='student')
        total_learners = learners.count()

        thirty_days_ago = timezone.now() - timedelta(days=30)
        active_learners = (
            LessonProgress.objects
            .filter(user__in=learners, updated_at__gte=thirty_days_ago)
            .values('user')
            .distinct()
            .count()
        )

        completed_lessons = LessonProgress.objects.filter(
            user__in=learners, completed=True
        )
        total_minutes = completed_lessons.aggregate(
            total=Sum('lesson__duration')
        )['total'] or 0

        # Course completion roughly estimated by checking if user completed all lessons
        # For simplicity in MV: we count unique courses where user has completed at least one lesson
        courses_touched = (
            completed_lessons.values('user', 'lesson__course')
            .distinct()
            .count()
        )

        data = {
            'camp_id': str(camp.id),
            'camp_name': camp.name,
            'total_learners': total_learners,
            'active_learners_30d': active_learners,
            'courses_completed': courses_touched,  # Simplified metric
            'total_learning_hours': round(total_minutes / 60, 1),
        }
        serializer = CampStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CourseStatsView(APIView):
    """GET /analytics/course/{course_id} — Analytics for a specific course."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise NotFound('Course not found')

        progress_records = LessonProgress.objects.filter(lesson__course=course)
        
        # Enrolled = users who started at least one lesson
        enrolled = progress_records.values('user').distinct().count()

        # Completed = users who completed all lessons in course
        # (Using a simplified count of completed lessons here for performance)
        total_lessons = course.lessons.count()
        completed = 0
        if total_lessons > 0:
            user_lesson_counts = (
                progress_records.filter(completed=True)
                .values('user')
                .annotate(completed_count=Count('lesson'))
            )
            completed = sum(
                1 for u in user_lesson_counts if u['completed_count'] >= total_lessons
            )

        # Average Quiz Score
        avg_score_pct = 0.0
        quizzes = QuizSubmission.objects.filter(quiz__lesson__course=course)
        if quizzes.exists():
            # calculate average percentage across all submissions
            total_submissions = quizzes.count()
            total_percentages = sum(
                (q.score / q.total * 100) if q.total > 0 else 0 
                for q in quizzes
            )
            avg_score_pct = total_percentages / total_submissions

        data = {
            'course_id': str(course.id),
            'course_title': course.title,
            'total_enrolled': enrolled,
            'total_completed': completed,
            'average_quiz_score': round(avg_score_pct, 1),
        }
        serializer = CourseStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
