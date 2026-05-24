from rest_framework.authentication import (
    BaseAuthentication
)

from rest_framework.exceptions import (
    AuthenticationFailed
)

from apps.authentication.api_keys.api_key_service import (
    APIKeyService
)


class APIKeyAuthentication(
    BaseAuthentication
):

    keyword = 'Api-Key'

    def authenticate(self, request):

        api_key = request.headers.get(
            'X-API-KEY'
        )

        if not api_key:
            return None

        user = APIKeyService.validate_key(
            api_key
        )

        if not user:

            raise AuthenticationFailed(
                'Invalid API Key'
            )

        return (user, None)