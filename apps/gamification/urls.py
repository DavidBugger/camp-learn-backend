from django.urls import path
from .views import PointsView, BadgesView, LeaderboardView

urlpatterns = [
    path('points/', PointsView.as_view(), name='gamification-points'),
    path('badges/', BadgesView.as_view(), name='gamification-badges'),
    path('leaderboard/', LeaderboardView.as_view(), name='gamification-leaderboard'),
]
