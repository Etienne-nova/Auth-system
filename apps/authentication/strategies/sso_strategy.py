from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from apps.users.models import User

from apps.authentication.providers.google_provider import (
    GoogleOAuthProvider
)

from .base_strategy import AuthenticationStrategy


class SSOAuthenticationStrategy(
    AuthenticationStrategy
):

    providers = {

        'google': GoogleOAuthProvider(),

    }

    def authenticate(self, **kwargs):

        provider_name = kwargs.get('provider')

        token = kwargs.get('token')

        provider = self.providers.get(provider_name)

        if not provider:
            raise Exception("Provider not supported")

        user_data = provider.verify_token(token)

        user, created = User.objects.get_or_create(

            email=user_data['email'],

            defaults={

                'username': user_data['username'],

                'is_email_verified': True,
            }
        )

        refresh = RefreshToken.for_user(user)

        return {

            'user': user,

            'access_token': str(refresh.access_token),

            'refresh_token': str(refresh)
        }