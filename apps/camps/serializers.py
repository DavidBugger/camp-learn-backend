from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Camp

User = get_user_model()


class CampSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Camp
        fields = ['id', 'name', 'location', 'state', 'country', 'created_at', 'user_count']
        read_only_fields = ['id', 'created_at']

    def get_user_count(self, obj):
        return obj.users.count()


class CampDetailSerializer(CampSerializer):
    facilitators = serializers.SerializerMethodField()

    class Meta(CampSerializer.Meta):
        fields = CampSerializer.Meta.fields + ['facilitators']

    def get_facilitators(self, obj):
        facilitators = obj.users.filter(role='facilitator')
        return [
            {'id': str(f.id), 'name': f.name, 'email': f.email}
            for f in facilitators
        ]


class FacilitatorAssignSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        if user.role not in ('facilitator', 'admin'):
            raise serializers.ValidationError(
                'User must be a facilitator or admin.'
            )
        return value
