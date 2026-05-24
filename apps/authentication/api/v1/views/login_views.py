from requests import request
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.authentication.api.v1.serializers.login_serializer import (
    LoginSerializer
)
from apps.authentication.utils.api_response import (
    ApiResponse
)
from apps.authentication.services.authenfication_service import AuthenticationService

from apps.authentication.audit.audit_service import (
    AuditService
)
from apps.authentication.security.throttles import (
    LoginRateThrottle
)
from drf_spectacular.utils import (
    extend_schema
)
from apps.authentication.devices.device_service import (
    DeviceService
)

from apps.authentication.devices.session_service import (
    SessionService
)
from apps.authentication.services.feature_service import (
    FeatureService
)
class LoginView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    

    @extend_schema(

        summary="User login",

        description=(
            "Authenticate user with "
            "email and password."
        ),

        tags=['Authentication']
    )
    
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = AuthenticationService.authenticate(
            strategy_name='password',
            **serializer.validated_data
        )
        #
        device = DeviceService.register_device(

            data['user'],

            request
        )
        
        if data['requires_mfa']:

            return Response(

                ApiResponse.success(

                    message='MFA required',

                    data={

                        'requires_mfa': True,

                        'user_id': data['user_id']
                    }

                ),

                status=status.HTTP_200_OK
            )
        SessionService.create_session(

            user=data['user'],

            device=device,

            refresh_token=data['refresh'],

            request=request
        )
        
        AuditService.log_event(
            
            event_type='login_success',
            
            request=request,
            
            user=data['user']
            
        )

        return Response(

            ApiResponse.success(

                message='Login successful',

                data={

                    'requires_mfa': False,

                    'access_token': data['access_token'],

                    'refresh_token': data['refresh_token'],

                    'user': {
                        'id': data['user'].id,
                        'email': data['user'].email,
                        'username': data['user'].username,
                    }

                }

            ),

            status=status.HTTP_200_OK
        )