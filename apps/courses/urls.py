from django.urls import path
from .views import CourseListCreateView, CourseDetailView, LessonListCreateView

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<uuid:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('<uuid:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
]
