from django.urls import reverse

from django.utils.http import (
    urlsafe_base64_encode
)

from django.utils.encoding import (
    force_bytes
)

from apps.authentication.password_reset.token_service import (
    password_reset_token_generator
)

from apps.authentication.tasks.email_tasks import (
    send_email_task
)


class PasswordResetService:

    @staticmethod
    def send_reset_email(user):

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = (
            password_reset_token_generator
            .make_token(user)
        )

        reset_link = (

            f"http://127.0.0.1:8000"

            f"{reverse('reset-password')}"

            f"?uid={uid}&token={token}"
        )

        subject = "Password Reset"

        message = (
            f"Hello {user.username},\n\n"
            f"Reset your password:\n"
            f"{reset_link}"
        )

        send_email_task.delay(

            subject,

            message,

            [user.email]
        )