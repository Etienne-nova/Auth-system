from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.users.models import User

from apps.authentication.api.v1.serializers.verify_otp_serializer import (
    VerifyOTPSerializer
)

from apps.authentication.mfa.mfa_service import (
    MFAService
)

from apps.authentication.utils.api_response import (
    ApiResponse
)
from apps.authentication.audit.audit_service import (
    AuditService
)
from apps.authentication.security.throttles import (
    MFARateThrottle
)
from drf_spectacular.utils import (
    extend_schema
)
class VerifyOTPView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [MFARateThrottle]
    
    @extend_schema(

        summary="Verify OTP",

        description=(
            "Verify user's OTP for MFA."
        ),

        tags=['Authentication']
    )

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            id=serializer.validated_data['user_id']
        ).first()

        if not user:

            return Response(

                ApiResponse.error(
                    message="User not found"
                ),

                status=status.HTTP_404_NOT_FOUND
            )

        tokens = MFAService.verify_otp(

            user=user,

            code=serializer.validated_data['code']
        )

        if not tokens:

            return Response(

                ApiResponse.error(
                    message="Invalid or expired OTP"
                ),

                status=status.HTTP_400_BAD_REQUEST
            )

        AuditService.log_event(
            user=user,
            event_type='verify_otp',
            request=request,
            #description='OTP verified successfully'
        )

        return Response(

            ApiResponse.success(

                message="OTP verified successfully",

                data=tokens
            ),

            status=status.HTTP_200_OK
        )