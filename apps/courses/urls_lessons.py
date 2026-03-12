from django.urls import path
from .views import LessonDetailView, LessonDownloadView

urlpatterns = [
    path('<uuid:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('<uuid:lesson_id>/download/', LessonDownloadView.as_view(), name='lesson-download'),
]
