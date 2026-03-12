from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    AdminUserSerializer,
    CreateFacilitatorSerializer,
)
from .permissions import IsAdmin, IsNotSuspended

User = get_user_model()


# ── Auth Views ───────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """POST /auth/register — Register a new user."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """POST /auth/logout — Blacklist the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Successfully logged out.'},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {'detail': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ── User Profile Views ──────────────────────────────────────────────────────

class UserProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /users/me — Retrieve or update current user profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]

    def get_object(self):
        return self.request.user


class UserProgressView(APIView):
    """GET /users/me/progress — Retrieve learner progress summary."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        from apps.progress.models import LessonProgress
        from apps.quizzes.models import QuizSubmission

        completed = LessonProgress.objects.filter(
            user=user, completed=True
        ).count()
        in_progress = LessonProgress.objects.filter(
            user=user, completed=False
        ).count()
        quizzes_taken = QuizSubmission.objects.filter(user=user).count()

        return Response({
            'lessons_completed': completed,
            'lessons_in_progress': in_progress,
            'quizzes_taken': quizzes_taken,
        })


# ── Admin Views ──────────────────────────────────────────────────────────────

class CreateFacilitatorView(generics.CreateAPIView):
    """POST /admin/facilitators — Create a facilitator account."""
    serializer_class = CreateFacilitatorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class ListUsersView(generics.ListAPIView):
    """GET /admin/users — List all users (admin only)."""
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'camp', 'is_suspended']
    search_fields = ['name', 'email', 'username']


class SuspendUserView(APIView):
    """POST /admin/users/{id}/suspend — Toggle user suspension."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.is_suspended = not user.is_suspended
        user.save(update_fields=['is_suspended'])
        action = 'suspended' if user.is_suspended else 'unsuspended'
        return Response({'detail': f'User {action} successfully.'})
