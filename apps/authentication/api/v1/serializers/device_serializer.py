from rest_framework import serializers

from apps.authentication.models import (
    UserDevice
)


class DeviceSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = UserDevice

        fields = '__all__'