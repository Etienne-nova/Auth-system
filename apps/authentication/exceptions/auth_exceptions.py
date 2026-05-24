from rest_framework.exceptions import APIException


class InvalidCredentialsException(APIException):

    status_code = 401

    default_detail = "Invalid credentials"

    default_code = "invalid_credentials"


class AuthenticationStrategyNotFoundException(APIException):

    status_code = 400

    default_detail = "Authentication strategy not found"

    default_code = "strategy_not_found"

class EmailNotVerifiedException(APIException):

    status_code = 403

    default_detail = "Email not verified"

    default_code = "email_not_verified"    


class AccountLockedException(APIException):

    status_code = 403

    default_detail = (
        "Too many failed attempts. "
        "Try again later."
    )

    default_code = "account_locked"    