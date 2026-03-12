from django.urls import path
from .views import CampListCreateView, CampDetailView, AssignFacilitatorView

urlpatterns = [
    path('', CampListCreateView.as_view(), name='camp-list-create'),
    path('<uuid:camp_id>/', CampDetailView.as_view(), name='camp-detail'),
    path('<uuid:camp_id>/facilitators/', AssignFacilitatorView.as_view(), name='camp-assign-facilitator'),
]
