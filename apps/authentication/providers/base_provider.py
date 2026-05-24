from abc import ABC, abstractmethod


class OAuthProvider(ABC):

    @abstractmethod
    def verify_token(self, token):
        pass