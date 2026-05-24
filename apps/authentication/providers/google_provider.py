from google.oauth2 import id_token

from google.auth.transport import requests

from apps.authentication.providers.base_provider import (
    OAuthProvider
)
from django.conf import settings

class GoogleOAuthProvider(OAuthProvider):
    
    #ici je dois remplacer par mon propre client id google
    CLIENT_ID = settings.GOOGLE_CLIENT_ID


    def verify_token(self, token):

        idinfo = id_token.verify_oauth2_token(

            token,

            requests.Request(),

            self.CLIENT_ID
        )

        return {

            'email': idinfo.get('email'),

            'username': idinfo.get('name'),

            'email_verified': idinfo.get(
                'email_verified',
                False
            )
        }