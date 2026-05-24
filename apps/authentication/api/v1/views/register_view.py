from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.authentication.api.v1.serializers.register_serializer import (
    RegisterSerializer
)
from apps.authentication.utils.api_response import (
    ApiResponse
)
from apps.authentication.services.registration_service import (
    RegistrationService
)
from drf_spectacular.utils import (
    extend_schema
)

class RegisterView(APIView):

    permission_classes = [AllowAny]
    
    @extend_schema(

        summary="User registration",

        description=(
            "Register a new user with "
            "email, username, and password."
        ),

        tags=['Authentication']
    )

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = RegistrationService.register_user(
            serializer.validated_data
        )

        return Response(

            ApiResponse.success(

                message='User registered successfully',

                data={

                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                    }

                }

            ),

            status=status.HTTP_201_CREATED
        )