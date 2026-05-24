from rest_framework import serializers


class VerifyOTPSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()

    code = serializers.CharField(max_length=6)