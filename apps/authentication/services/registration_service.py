from apps.users.models import User

from apps.authentication.email.email_service import (
    EmailService
)

class RegistrationService:

    @staticmethod
    def register_user(validated_data):

        validated_data.pop('confirm_password')

        password = validated_data.pop('password')

        user = User.objects.create_user(

            password=password,

            is_active=True,

            is_email_verified=False,

            **validated_data
        )

        EmailService.send_verification_email(user)

        return user