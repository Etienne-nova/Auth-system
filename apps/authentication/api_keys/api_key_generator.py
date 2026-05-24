import secrets

import hashlib


class APIKeyGenerator:

    @staticmethod
    def generate_api_key():

        raw_key = secrets.token_urlsafe(32)

        hashed_key = hashlib.sha256(

            raw_key.encode()

        ).hexdigest()

        key_prefix = raw_key[:8]

        return {

            'raw_key': raw_key,

            'hashed_key': hashed_key,

            'key_prefix': key_prefix
        }