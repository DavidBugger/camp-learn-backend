from rest_framework import generics, permissions

from apps.accounts.permissions import IsFacilitator
from .models import Course, Lesson
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    LessonSerializer,
    LessonDownloadSerializer,
)


# ── Course Views ─────────────────────────────────────────────────────────────

class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET  /courses — List all courses
    POST /courses — Create course (facilitator+)
    """
    queryset = Course.objects.all()
    filterset_fields = ['category']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        return CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsFacilitator()]
        return [permissions.IsAuthenticated()]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /courses/{course_id} — Course details with lessons
    PUT    /courses/{course_id} — Update course
    DELETE /courses/{course_id} — Delete course
    """
    queryset = Course.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'course_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsFacilitator()]


# ── Lesson Views ─────────────────────────────────────────────────────────────

class LessonListCreateView(generics.ListCreateAPIView):
    """
    GET  /courses/{course_id}/lessons — List lessons
    POST /courses/{course_id}/lessons — Create lesson
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsFacilitator()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /lessons/{lesson_id} — Lesson details
    PUT    /lessons/{lesson_id} — Update lesson
    DELETE /lessons/{lesson_id} — Delete lesson
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'lesson_id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsFacilitator()]


class LessonDownloadView(generics.RetrieveAPIView):
    """GET /lessons/{lesson_id}/download — Download lesson for offline."""
    queryset = Lesson.objects.all()
    serializer_class = LessonDownloadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'lesson_id'
