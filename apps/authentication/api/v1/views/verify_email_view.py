from django.utils.http import (
    urlsafe_base64_decode
)

from django.utils.encoding import force_str

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.users.models import User

from apps.authentication.email.token_services import (
    email_verification_token
)

from apps.authentication.utils.api_response import (
    ApiResponse
)
from apps.authentication.audit.audit_service import AuditService

from drf_spectacular.utils import (
    extend_schema
)

class VerifyEmailView(APIView):

    permission_classes = [AllowAny]
    
    @extend_schema(

        summary="Verify Email",

        description=(
            "Verify user's email address with "
            "the provided verification link."
        ),

        tags=['Authentication']
    )

    def get(self, request):

        uid = request.GET.get('uid')

        token = request.GET.get('token')

        try:

            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(pk=user_id)

        except Exception:

            return Response(

                ApiResponse.error(
                    message="Invalid verification link"
                ),

                status=status.HTTP_400_BAD_REQUEST
            )

        if not email_verification_token.check_token(
            user,
            token
        ):

            return Response(

                ApiResponse.error(
                    message="Invalid or expired token"
                ),

                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True

        user.save()
        
        AuditService.log_event(

            event_type='email_verified',

            request=request,

            user=user
        )

        return Response(

            ApiResponse.success(
                message="Email verified successfully"
            ),

            status=status.HTTP_200_OK
        )