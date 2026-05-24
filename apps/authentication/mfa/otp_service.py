import random

from django.utils import timezone

from datetime import timedelta

from apps.authentication.models import OTPCode
from apps.authentication.tasks.otp_tasks import (
    send_otp_email_task
)

class OTPService:

    OTP_LENGTH = 6

    OTP_EXPIRATION_MINUTES = 5

    @staticmethod
    def generate_otp():

        return str(
            random.randint(100000, 999999)
        )

    @classmethod
    def create_otp(cls, user):
        #
        send_otp_email_task.delay(

            user.email,

            code
        )

        OTPCode.objects.filter(
            user=user,
            is_used=False
        ).delete()

        code = cls.generate_otp()

        otp = OTPCode.objects.create(

            user=user,

            code=code,

            expires_at=timezone.now() + timedelta(
                minutes=cls.OTP_EXPIRATION_MINUTES
            )
        )

        return otp
    
        