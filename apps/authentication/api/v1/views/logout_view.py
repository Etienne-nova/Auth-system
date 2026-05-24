from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from apps.authentication.api.v1.serializers.logout_serializer import (
    LogoutSerializer
)

from apps.authentication.services.logout_service import (
    LogoutService
)

from apps.authentication.utils.api_response import (
    ApiResponse
)
from apps.authentication.audit.audit_service import (
    AuditService
)
from drf_spectacular.utils import (
    extend_schema
)
class LogoutView(APIView):
    
    @extend_schema(

        summary="User logout",

        description=(
            "Logout the currently authenticated user."
        ),

        tags=['Authentication']
    )

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        LogoutService.logout(

            serializer.validated_data[
                'refresh_token'
            ]
        )
        AuditService.log_event(
            user=request.user,
            event_type='logout',
            request=request,
            #description='User logged out successfully'
        )
        return Response(

            ApiResponse.success(
                message='Logout successful'
            ),

            status=status.HTTP_200_OK
        )