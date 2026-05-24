from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from apps.authentication.models import OTPCode


class MFAService:

    @staticmethod
    def verify_otp(user, code):

        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            is_used=False
        ).first()

        if not otp:
            return None

        if otp.is_expired():
            return None

        otp.is_used = True

        otp.save()

        refresh = RefreshToken.for_user(user)

        return {

            'access_token': str(refresh.access_token),

            'refresh_token': str(refresh)
        }