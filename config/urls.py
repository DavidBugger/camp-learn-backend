"""
CampLearn URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

def health_check(request):
    return JsonResponse({"status": "healthy", "platform": "CampLearn"})

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include([
        path('auth/', include('apps.accounts.urls_auth')),
        path('users/', include('apps.accounts.urls_users')),
        path('admin-api/', include('apps.accounts.urls_admin')),
        path('camps/', include('apps.camps.urls')),
        path('courses/', include('apps.courses.urls')),
        path('lessons/', include('apps.courses.urls_lessons')),
        path('quiz/', include('apps.quizzes.urls_quiz')),
        path('', include('apps.quizzes.urls_lessons')),
        path('progress/', include('apps.progress.urls')),
        path('gamification/', include('apps.gamification.urls')),
        path('devices/', include('apps.devices.urls')),
        path('analytics/', include('apps.analytics.urls')),
    ])),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
