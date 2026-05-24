from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from apps.authentication.models import (
    UserDevice
)

from apps.authentication.api.v1.serializers.device_serializer import (
    DeviceSerializer
)


class DeviceListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        devices = UserDevice.objects.filter(
            user=request.user
        )

        serializer = DeviceSerializer(
            devices,
            many=True
        )

        return Response(serializer.data)