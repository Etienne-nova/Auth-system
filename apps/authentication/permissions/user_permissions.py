from apps.authentication.permissions.has_permission import (
    HasPermission
)


class CanManageUsers(HasPermission):

    permission_code = 'manage_users'


class CanDeleteUsers(HasPermission):

    permission_code = 'delete_users'