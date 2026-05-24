from rest_framework import serializers


class CreateAPIKeySerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=255
    )