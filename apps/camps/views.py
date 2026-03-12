from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.accounts.permissions import IsAdmin, IsFacilitator
from .models import Camp
from .serializers import CampSerializer, CampDetailSerializer, FacilitatorAssignSerializer

User = get_user_model()


class CampListCreateView(generics.ListCreateAPIView):
    """
    GET  /camps — List all camps
    POST /camps — Create a new camp (admin only)
    """
    queryset = Camp.objects.all()
    serializer_class = CampSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


class CampDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /camps/{camp_id} — Camp details
    PUT    /camps/{camp_id} — Update camp
    DELETE /camps/{camp_id} — Delete camp
    """
    queryset = Camp.objects.all()
    serializer_class = CampDetailSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'camp_id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdmin()]


class AssignFacilitatorView(generics.GenericAPIView):
    """POST /camps/{camp_id}/facilitators — Assign facilitator to camp."""
    serializer_class = FacilitatorAssignSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, camp_id):
        try:
            camp = Camp.objects.get(pk=camp_id)
        except Camp.DoesNotExist:
            return Response(
                {'detail': 'Camp not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(pk=serializer.validated_data['user_id'])
        user.camp = camp
        user.save(update_fields=['camp'])

        return Response(
            {'detail': f'{user.name} assigned to {camp.name}.'},
            status=status.HTTP_200_OK,
        )
