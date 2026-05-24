from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework import status

from apps.authentication.models import (
    UserSession
)

from apps.authentication.utils.api_response import (
    ApiResponse
)


class RevokeDeviceView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):

        session = UserSession.objects.filter(

            id=session_id,

            user=request.user

        ).first()

        if not session:

            return Response(

                ApiResponse.error(
                    message="Session not found"
                ),

                status=status.HTTP_404_NOT_FOUND
            )

        session.is_active = False

        session.save()

        return Response(

            ApiResponse.success(
                message="Session revoked"
            )
        )