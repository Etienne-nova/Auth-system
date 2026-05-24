from urllib import request

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication import email

from .base_strategy import AuthenticationStrategy

from apps.authentication.exceptions.auth_exceptions import (
    InvalidCredentialsException, EmailNotVerifiedException
)
from apps.authentication.mfa.otp_service import (
    OTPService
)
from apps.authentication.audit.audit_service import (
    AuditService
)
from apps.authentication.security.brute_force_service import (
    BruteForceService
)

from apps.authentication.exceptions.auth_exceptions import (
    AccountLockedException
)
class PasswordAuthenticationStrategy(AuthenticationStrategy):
    
    
    def authenticate(self, request=None, **kwargs):
        if BruteForceService.is_blocked(
            email,
            request
        ):
            raise AccountLockedException()


        email = kwargs.get('email')

        password = kwargs.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            AuditService.log_event(

                event_type='login_failed',

                request=request,

                metadata={
                    'email': email
                }
            )
            
            BruteForceService.register_failed_attempt(
                email,
                request
            )
            
            raise InvalidCredentialsException()


        if not user.is_email_verified:
            
            BruteForceService.reset_attempts(
                email,
                request
            )
            raise EmailNotVerifiedException()

        refresh = RefreshToken.for_user(user)

        if user.is_mfa_enabled:

            otp = OTPService.create_otp(user)

            print(f"OTP CODE: {otp.code}")

            return {

                'requires_mfa': True,

                'message': 'OTP sent',

                'user_id': user.id
            }

        refresh = RefreshToken.for_user(user)

        return {

            'requires_mfa': False,

            'user': user,

            'access_token': str(refresh.access_token),

            'refresh_token': str(refresh)
        }