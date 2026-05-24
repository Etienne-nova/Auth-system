from apps.authentication.config.auth_features import (
    AUTH_FEATURES
)


class FeatureService:

    @staticmethod
    def is_enabled(feature_name):

        return AUTH_FEATURES.get(
            feature_name,
            False
        )