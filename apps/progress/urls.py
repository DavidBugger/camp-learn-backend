from django.urls import path
from .views import MarkLessonCompleteView, CourseProgressView, LearningStatsView

urlpatterns = [
    path('lesson/', MarkLessonCompleteView.as_view(), name='progress-mark-complete'),
    path('course/<uuid:course_id>/', CourseProgressView.as_view(), name='progress-course'),
    path('statistics/', LearningStatsView.as_view(), name='progress-statistics'),
]
