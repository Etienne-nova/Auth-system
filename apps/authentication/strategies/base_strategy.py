from abc import ABC, abstractmethod


class AuthenticationStrategy(ABC):

    @abstractmethod
    def authenticate(self, **kwargs):
        pass