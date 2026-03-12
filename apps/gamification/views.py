from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PointTransaction, UserBadge
from .serializers import (
    UserBadgeSerializer,
    PointTransactionSerializer,
)

User = get_user_model()


class PointsView(APIView):
    """GET /gamification/points — Retrieve learner points and history."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = PointTransaction.objects.filter(user=request.user)[:20]
        total = (
            PointTransaction.objects.filter(user=request.user)
            .aggregate(total=Sum('points'))['total']
        ) or 0

        return Response({
            'total_points': total,
            'recent_transactions': PointTransactionSerializer(
                transactions, many=True
            ).data,
        })


class BadgesView(generics.ListAPIView):
    """GET /gamification/badges — Retrieve badges earned by current user."""
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(
            user=self.request.user
        ).select_related('badge')


class LeaderboardView(APIView):
    """GET /gamification/leaderboard — Top learners by points."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        leaders = (
            User.objects.filter(role='student')
            .annotate(total_points=Sum('point_transactions__points'))
            .exclude(total_points=None)
            .order_by('-total_points')[:20]
        )

        data = [
            {
                'rank': idx + 1,
                'user_id': str(user.id),
                'name': user.name or user.username,
                'total_points': user.total_points or 0,
            }
            for idx, user in enumerate(leaders)
        ]

        return Response(data)
