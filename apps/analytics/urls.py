from django.urls import path
from .views import PlatformStatsView, CampStatsView, CourseStatsView

urlpatterns = [
    path('platform/', PlatformStatsView.as_view(), name='analytics-platform'),
    path('camp/<uuid:camp_id>/', CampStatsView.as_view(), name='analytics-camp'),
    path('course/<uuid:course_id>/', CourseStatsView.as_view(), name='analytics-course'),
]
