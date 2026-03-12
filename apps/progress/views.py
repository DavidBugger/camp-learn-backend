from django.utils import timezone
from django.db.models import Sum
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course, Lesson
from apps.quizzes.models import QuizSubmission
from .models import LessonProgress
from .serializers import (
    MarkLessonCompleteSerializer,
    CourseProgressSerializer,
    LearningStatsSerializer,
)


class MarkLessonCompleteView(APIView):
    """POST /progress/lesson — Mark a lesson as completed."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MarkLessonCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson_id = serializer.validated_data['lesson_id']
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {'detail': 'Lesson not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'completed': True, 'completion_time': timezone.now()},
        )
        if not created and not progress.completed:
            progress.completed = True
            progress.completion_time = timezone.now()
            progress.save(update_fields=['completed', 'completion_time', 'updated_at'])

        return Response({
            'detail': 'Lesson marked as completed.',
            'lesson_id': str(lesson.id),
            'completed': progress.completed,
        })


class CourseProgressView(APIView):
    """GET /progress/course/{course_id} — Course progress for current user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {'detail': 'Course not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        total_lessons = course.lessons.count()
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True,
        ).count()

        percentage = 0
        if total_lessons > 0:
            percentage = round((completed_lessons / total_lessons) * 100, 1)

        return Response({
            'course_id': str(course.id),
            'course_title': course.title,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'percentage': percentage,
        })


class LearningStatsView(APIView):
    """GET /progress/statistics — Overall learning statistics for current user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        total_completed = LessonProgress.objects.filter(
            user=user, completed=True
        ).count()

        courses_started = (
            LessonProgress.objects.filter(user=user)
            .values('lesson__course')
            .distinct()
            .count()
        )

        quizzes_taken = QuizSubmission.objects.filter(user=user).count()

        # Estimate learning hours from completed lesson durations
        total_minutes = (
            LessonProgress.objects.filter(user=user, completed=True)
            .select_related('lesson')
            .aggregate(total=Sum('lesson__duration'))['total']
        ) or 0
        learning_hours = round(total_minutes / 60, 1)

        return Response({
            'total_lessons_completed': total_completed,
            'total_courses_started': courses_started,
            'total_quizzes_taken': quizzes_taken,
            'total_learning_hours': learning_hours,
        })
