from django.utils import timezone

from datetime import timedelta

from apps.authentication.models import (
    LoginAttempt
)

from apps.authentication.security.security_constants import (
    MAX_LOGIN_ATTEMPTS,
    LOCKOUT_TIME_MINUTES
)


class BruteForceService:

    @staticmethod
    def get_client_ip(request):

        return request.META.get(
            'REMOTE_ADDR'
        )

    @classmethod
    def is_blocked(cls, email, request):

        ip = cls.get_client_ip(request)

        attempt = LoginAttempt.objects.filter(

            email=email,

            ip_address=ip

        ).first()

        if not attempt:
            return False

        if (
            attempt.is_blocked
            and attempt.blocked_until
            and timezone.now() < attempt.blocked_until
        ):
            return True

        return False

    @classmethod
    def register_failed_attempt(
        cls,
        email,
        request
    ):

        ip = cls.get_client_ip(request)

        attempt, created = (
            LoginAttempt.objects.get_or_create(

                email=email,

                ip_address=ip
            )
        )

        attempt.attempts += 1

        if attempt.attempts >= MAX_LOGIN_ATTEMPTS:

            attempt.is_blocked = True

            attempt.blocked_until = (
                timezone.now()
                + timedelta(
                    minutes=LOCKOUT_TIME_MINUTES
                )
            )

        attempt.save()

    @classmethod
    def reset_attempts(cls, email, request):

        ip = cls.get_client_ip(request)

        LoginAttempt.objects.filter(

            email=email,

            ip_address=ip

        ).delete()