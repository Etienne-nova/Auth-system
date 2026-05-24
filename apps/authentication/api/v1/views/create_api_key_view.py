from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from apps.authentication.api.v1.serializers.create_api_key_serializer import (
    CreateAPIKeySerializer
)

from apps.authentication.api_keys.api_key_service import (
    APIKeyService
)

from apps.authentication.utils.api_response import (
    ApiResponse
)


class CreateAPIKeyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = (
            CreateAPIKeySerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = (
            APIKeyService.create_api_key(

                request.user,

                serializer.validated_data[
                    'name'
                ]
            )
        )

        return Response(

            ApiResponse.success(

                message=(
                    "API Key created"
                ),

                data={

                    'api_key': result[
                        'raw_key'
                    ]
                }
            )
        )