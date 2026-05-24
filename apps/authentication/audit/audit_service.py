from apps.authentication.models import AuditLog


class AuditService:

    @staticmethod
    def log_event(

        event_type,

        request=None,

        user=None,

        metadata=None
    ):

        ip_address = None

        user_agent = None

        if request:

            ip_address = request.META.get(
                'REMOTE_ADDR'
            )

            user_agent = request.META.get(
                'HTTP_USER_AGENT'
            )

        AuditLog.objects.create(

            user=user,

            event_type=event_type,

            ip_address=ip_address,

            user_agent=user_agent,

            metadata=metadata or {}
        )