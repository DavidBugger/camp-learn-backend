from django.urls import path
from .views import UserProfileView, UserProgressView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/progress/', UserProgressView.as_view(), name='user-progress'),
]
