from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'name', 'phone',
            'role', 'camp', 'password', 'password_confirm',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    camp_name = serializers.CharField(source='camp.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'name', 'phone',
            'role', 'camp', 'camp_name', 'date_joined',
        ]
        read_only_fields = ['id', 'email', 'role', 'date_joined']


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin user listing."""
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'name', 'phone',
            'role', 'camp', 'is_suspended', 'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']


class CreateFacilitatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'name', 'phone',
            'camp', 'password',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = User.Role.FACILITATOR
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
