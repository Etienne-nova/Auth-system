class PermissionService:

    @staticmethod
    def user_has_permission(
        user,
        permission_code
    ):

        if user.is_superuser:
            return True

        return user.roles.filter(

            permissions__code=permission_code

        ).exists()