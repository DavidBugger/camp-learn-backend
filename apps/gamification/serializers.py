from rest_framework import serializers
from .models import Badge, UserBadge, PointTransaction


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon_url', 'criteria']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'awarded_at']


class PointTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointTransaction
        fields = ['id', 'points', 'reason', 'description', 'created_at']


class LeaderboardEntrySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    name = serializers.CharField()
    total_points = serializers.IntegerField()
    rank = serializers.IntegerField()
