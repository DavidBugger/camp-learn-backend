from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allow access to camp admins and system admins."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('admin', 'system_admin')
        )


class IsSystemAdmin(permissions.BasePermission):
    """Allow access to system admins only."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'system_admin'
        )


class IsFacilitator(permissions.BasePermission):
    """Allow access to facilitators and above."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('facilitator', 'admin', 'system_admin')
        )


class IsStudent(permissions.BasePermission):
    """Allow access to students."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'student'
        )


class IsNotSuspended(permissions.BasePermission):
    """Deny access to suspended users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_suspended
        )
