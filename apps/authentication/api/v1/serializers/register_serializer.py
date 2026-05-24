from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match"
                }
            )

        return attrs