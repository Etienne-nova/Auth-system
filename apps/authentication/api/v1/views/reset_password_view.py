from django.utils.http import (
    urlsafe_base64_decode
)

from django.utils.encoding import (
    force_str
)

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from rest_framework import status

from apps.users.models import User

from apps.authentication.password_reset.token_service import (
    password_reset_token_generator
)

from apps.authentication.api.v1.serializers.reset_password_serializer import (
    ResetPasswordSerializer
)

from apps.authentication.utils.api_response import (
    ApiResponse
)


class ResetPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            user_id = force_str(

                urlsafe_base64_decode(

                    serializer.validated_data[
                        'uid'
                    ]
                )
            )

            user = User.objects.get(
                pk=user_id
            )

        except Exception:

            return Response(

                ApiResponse.error(
                    message="Invalid reset link"
                ),

                status=status.HTTP_400_BAD_REQUEST
            )

        token_is_valid = (
            password_reset_token_generator
            .check_token(
                user,
                serializer.validated_data[
                    'token'
                ]
            )
        )

        if not token_is_valid:

            return Response(

                ApiResponse.error(
                    message=(
                        "Invalid or expired token"
                    )
                ),

                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(

            serializer.validated_data[
                'password'
            ]
        )

        user.save()

        return Response(

            ApiResponse.success(
                message=(
                    "Password reset successful"
                )
            ),

            status=status.HTTP_200_OK
        )