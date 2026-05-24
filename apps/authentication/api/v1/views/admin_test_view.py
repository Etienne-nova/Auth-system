from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from apps.authentication.permissions.user_permissions import (
    CanManageUsers
)

from apps.authentication.utils.api_response import (
    ApiResponse
)


class AdminTestView(APIView):

    permission_classes = [CanManageUsers]

    def get(self, request):

        return Response(

            ApiResponse.success(

                message='Access granted'

            ),

            status=status.HTTP_200_OK
        )