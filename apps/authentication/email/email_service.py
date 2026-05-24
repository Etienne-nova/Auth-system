from django.core.mail import send_mail

from django.conf import settings

from django.urls import reverse

from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_bytes

from apps.authentication.email.token_services import (
    email_verification_token
)
from apps.authentication.tasks.email_tasks import (
    send_email_task
)

class EmailService:

    @staticmethod
    def send_verification_email(user):

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = email_verification_token.make_token(user)

        verification_link = (
            f"http://127.0.0.1:8000"
            f"{reverse('verify-email')}?uid={uid}&token={token}"
        )

        subject = "Verify your email"

        message = (
            f"Hello {user.username},\n\n"
            f"Verify your account:\n"
            f"{verification_link}"
        )

        send_email_task.delay(
            subject,
            message,
           # settings.DEFAULT_FROM_EMAIL,
            [user.email],
            #fail_silently=False
        )