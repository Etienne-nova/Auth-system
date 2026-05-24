from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.authentication.api.v1.serializers.sso_serializer import (
    SSOSerializer
)

from apps.authentication.services.authenfication_service import (
    AuthenticationService
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

class SSOLoginView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(

        summary="SSO login",

        description=(
            "Login user via SSO provider."
        ),

        tags=['Authentication']
    )

    def post(self, request):

        serializer = SSOSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = AuthenticationService.authenticate(

            strategy_name='sso',

            **serializer.validated_data
        )
        
        AuditService.log_event(

            event_type='sso_login',

            request=request,

            user=data['user'],

            metadata={
                'provider': serializer.validated_data[
                    'provider'
                ]
            }
        )

        return Response(

            ApiResponse.success(

                message='SSO login successful',

                data={

                    'access_token': data[
                        'access_token'
                    ],

                    'refresh_token': data[
                        'refresh_token'
                    ],

                    'user': {
                        'id': data['user'].id,
                        'email': data['user'].email,
                        'username': data['user'].username,
                    }
                }

            ),

            status=status.HTTP_200_OK
        )