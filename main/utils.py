from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def check_permissions(required_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
         
            if request.user.is_superuser:
                logger.debug(f"Superuser {request.user.username} bypassing permission checks.")
                return view_func(request, *args, **kwargs)

            user_permissions = set()
            for group in request.user.groups.all():
                perms = group.permissions.all().values_list('content_type__app_label', 'codename')
                user_permissions.update([f"{app_label}.{codename}" for app_label, codename in perms])
                logger.debug(f"Group Permissions for {group.name}: {perms}")

            user_specific_perms = request.user.user_permissions.all().values_list('content_type__app_label', 'codename')
            user_permissions.update([f"{app_label}.{codename}" for app_label, codename in user_specific_perms])
            logger.debug(f"Specific Permissions for {request.user.username}: {user_specific_perms}")

            required_permissions_set = set(required_permissions)
            logger.debug(f"User {request.user.username} permissions: {user_permissions}")
            logger.debug(f"Required permissions: {required_permissions_set}")

            if not user_permissions.issuperset(required_permissions_set):
                logger.debug(f"User permissions: {user_permissions}")
                logger.debug(f"Missing permissions: {required_permissions_set - user_permissions}")
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
