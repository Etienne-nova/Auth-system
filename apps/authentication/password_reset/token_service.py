from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator
)


class PasswordResetTokenGeneratorService(
    PasswordResetTokenGenerator
):
    pass


password_reset_token_generator = (
    PasswordResetTokenGeneratorService()
)