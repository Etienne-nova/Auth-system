from rest_framework.permissions import BasePermission

from apps.authentication.services.permission_service import (
    PermissionService
)


class HasPermission(BasePermission):

    permission_code = None

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return PermissionService.user_has_permission(

            request.user,

            self.permission_code
        )