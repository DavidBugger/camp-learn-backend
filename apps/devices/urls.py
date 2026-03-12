from django.urls import path
from .views import RegisterDeviceView, SyncUploadView, ContentUpdatesView

urlpatterns = [
    path('register/', RegisterDeviceView.as_view(), name='device-register'),
    path('sync/', SyncUploadView.as_view(), name='device-sync'),
    path('updates/', ContentUpdatesView.as_view(), name='device-updates'),
]
