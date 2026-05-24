from rest_framework import serializers


class SSOSerializer(serializers.Serializer):

    provider = serializers.CharField()

    token = serializers.CharField()