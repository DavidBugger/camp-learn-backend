import uuid
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course, Lesson
from apps.courses.serializers import CourseSerializer, LessonSerializer
from apps.progress.models import LessonProgress
from apps.quizzes.models import Quiz, QuizSubmission, Question
from .models import Device, SyncLog
from .serializers import (
    DeviceRegisterSerializer,
    SyncUploadSerializer,
)


class RegisterDeviceView(generics.CreateAPIView):
    """POST /devices/register — Register a device for the current user."""
    serializer_class = DeviceRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SyncUploadView(APIView):
    """POST /devices/sync — Upload offline activity data."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SyncUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Find device
        try:
            device = Device.objects.get(
                device_identifier=data['device_identifier'],
                user=request.user,
            )
        except Device.DoesNotExist:
            return Response(
                {'detail': 'Device not registered.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        sync_log = SyncLog.objects.create(
            device=device,
            sync_status='in_progress',
        )

        records_uploaded = 0

        try:
            # Process lesson completions
            for item in data.get('lesson_completions', []):
                lesson_id = item.get('lesson_id')
                try:
                    lesson = Lesson.objects.get(pk=lesson_id)
                except Lesson.DoesNotExist:
                    continue

                progress, created = LessonProgress.objects.get_or_create(
                    user=request.user,
                    lesson=lesson,
                    defaults={
                        'completed': True,
                        'completion_time': item.get('completed_at', timezone.now()),
                    },
                )
                if not created and not progress.completed:
                    progress.completed = True
                    progress.completion_time = item.get('completed_at', timezone.now())
                    progress.save(update_fields=['completed', 'completion_time'])
                records_uploaded += 1

            # Process quiz submissions
            for item in data.get('quiz_submissions', []):
                quiz_id = item.get('quiz_id')
                submission_uid = item.get('submission_uid', str(uuid.uuid4()))

                # Skip duplicates
                if QuizSubmission.objects.filter(submission_uid=submission_uid).exists():
                    continue

                try:
                    quiz = Quiz.objects.prefetch_related('questions').get(pk=quiz_id)
                except Quiz.DoesNotExist:
                    continue

                answers = item.get('answers', {})
                score = 0
                total = quiz.questions.count()
                for question in quiz.questions.all():
                    if answers.get(str(question.id), '').lower() == question.correct_answer.lower():
                        score += 1

                QuizSubmission.objects.create(
                    user=request.user,
                    quiz=quiz,
                    score=score,
                    total=total,
                    answers=answers,
                    submission_uid=submission_uid,
                )
                records_uploaded += 1

            # Update device and sync log
            device.last_sync = timezone.now()
            device.save(update_fields=['last_sync'])

            sync_log.sync_status = 'completed'
            sync_log.records_uploaded = records_uploaded
            sync_log.save(update_fields=['sync_status', 'records_uploaded'])

            return Response({
                'detail': 'Sync completed successfully.',
                'records_uploaded': records_uploaded,
                'sync_id': str(sync_log.id),
            })

        except Exception as e:
            sync_log.sync_status = 'failed'
            sync_log.error_message = str(e)
            sync_log.save(update_fields=['sync_status', 'error_message'])
            return Response(
                {'detail': f'Sync failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ContentUpdatesView(APIView):
    """GET /devices/updates — Get new/updated content since last sync."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        since = request.query_params.get('since')

        if since:
            from django.utils.dateparse import parse_datetime
            since_dt = parse_datetime(since)
        else:
            # Get from device's last_sync
            device_id = request.query_params.get('device_identifier')
            if device_id:
                try:
                    device = Device.objects.get(
                        device_identifier=device_id,
                        user=request.user,
                    )
                    since_dt = device.last_sync
                except Device.DoesNotExist:
                    since_dt = None
            else:
                since_dt = None

        if since_dt:
            new_courses = Course.objects.filter(created_at__gt=since_dt)
            new_lessons = Lesson.objects.filter(created_at__gt=since_dt)
        else:
            new_courses = Course.objects.all()
            new_lessons = Lesson.objects.all()

        return Response({
            'new_courses': CourseSerializer(new_courses, many=True).data,
            'new_lessons': LessonSerializer(new_lessons, many=True).data,
            'server_time': timezone.now().isoformat(),
        })
