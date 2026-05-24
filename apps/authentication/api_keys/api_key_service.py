import hashlib

from django.utils import timezone

from apps.authentication.models import (
    APIKey
)

from apps.authentication.api_keys.api_key_generator import (
    APIKeyGenerator
)


class APIKeyService:

    @staticmethod
    def create_api_key(

        user,

        name
    ):

        generated = (
            APIKeyGenerator.generate_api_key()
        )

        api_key = APIKey.objects.create(

            name=name,

            key_prefix=generated[
                'key_prefix'
            ],

            hashed_key=generated[
                'hashed_key'
            ],

            user=user
        )

        return {

            'api_key': api_key,

            'raw_key': generated[
                'raw_key'
            ]
        }

    @staticmethod
    def validate_key(raw_key):

        hashed_key = hashlib.sha256(

            raw_key.encode()

        ).hexdigest()

        api_key = APIKey.objects.filter(

            hashed_key=hashed_key,

            is_active=True

        ).first()

        if not api_key:
            return None

        if (
            api_key.expires_at
            and timezone.now()
            > api_key.expires_at
        ):
            return None

        api_key.last_used_at = timezone.now()

        api_key.save()

        return api_key.user