from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from rest_framework import status

from apps.users.models import User

from apps.authentication.api.v1.serializers.forgot_password_serializer import (
    ForgotPasswordSerializer
)

from apps.authentication.password_reset.password_reset_service import (
    PasswordResetService
)

from apps.authentication.utils.api_response import (
    ApiResponse
)


class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = (
            ForgotPasswordSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = User.objects.filter(

            email=serializer.validated_data[
                'email'
            ]

        ).first()

        if user:

            PasswordResetService.send_reset_email(
                user
            )

        return Response(

            ApiResponse.success(

                message=(
                    "If the email exists, "
                    "a reset link has been sent."
                )
            ),

            status=status.HTTP_200_OK
        )