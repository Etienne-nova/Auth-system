import re


class PasswordValidator:

    @staticmethod
    def validate(password):

        if len(password) < 8:
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[0-9]", password):
            return False

        return True