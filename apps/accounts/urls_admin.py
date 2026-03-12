from django.urls import path
from .views import CreateFacilitatorView, ListUsersView, SuspendUserView

urlpatterns = [
    path('facilitators/', CreateFacilitatorView.as_view(), name='admin-create-facilitator'),
    path('users/', ListUsersView.as_view(), name='admin-list-users'),
    path('users/<uuid:user_id>/suspend/', SuspendUserView.as_view(), name='admin-suspend-user'),
]
