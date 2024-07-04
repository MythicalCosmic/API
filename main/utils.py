# utils.py

from rest_framework import permissions


class IsInGroup(permissions.BasePermission):
    """
    Custom permission to only allow users in a specific group.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        required_group = getattr(view, 'required_group', None)
        if required_group:
            return request.user.groups.filter(name=required_group).exists()
        return False
