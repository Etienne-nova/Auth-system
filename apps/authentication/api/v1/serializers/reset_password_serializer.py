from rest_framework import serializers


class ResetPasswordSerializer(
    serializers.Serializer
):

    uid = serializers.CharField()

    token = serializers.CharField()

    password = serializers.CharField(
        min_length=8
    )

    confirm_password = serializers.CharField()

    def validate(self, attrs):

        if (
            attrs['password']
            != attrs['confirm_password']
        ):
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return attrs