from django.utils import timezone

from datetime import timedelta

from apps.authentication.models import (
    UserSession
)


class SessionService:

    @staticmethod
    def create_session(

        user,

        device,

        refresh_token,

        request
    ):

        expires_at = (
            timezone.now()
            + timedelta(days=7)
        )

        return UserSession.objects.create(

            user=user,

            device=device,

            refresh_token=str(refresh_token),

            ip_address=request.META.get(
                'REMOTE_ADDR'
            ),

            expires_at=expires_at
        )

    @staticmethod
    def revoke_session(session):

        session.is_active = False

        session.save()