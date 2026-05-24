from apps.authentication.strategies.password_strategy import (
    PasswordAuthenticationStrategy
)

from apps.authentication.exceptions.auth_exceptions import (
    AuthenticationStrategyNotFoundException
)
from apps.authentication.strategies.sso_strategy import (
    SSOAuthenticationStrategy
)
class AuthenticationService:

    strategies = {

        'password': PasswordAuthenticationStrategy(),
        'sso': SSOAuthenticationStrategy(),

    }

    @classmethod
    def authenticate(cls, strategy_name, request=None, **kwargs):

        strategy = cls.strategies.get(strategy_name)

        if not strategy:
            raise Exception("Authentication strategy not found")
            raise AuthenticationStrategyNotFoundException()

        return strategy.authenticate(request=request, **kwargs)