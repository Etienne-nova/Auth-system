import user_agents

from apps.authentication.models import (
    UserDevice
)


class DeviceService:

    @staticmethod
    def register_device(

        user,

        request
    ):

        user_agent_string = request.META.get(
            'HTTP_USER_AGENT',
            ''
        )

        ip_address = request.META.get(
            'REMOTE_ADDR'
        )

        ua = user_agents.parse(
            user_agent_string
        )

        device_name = (
            f"{ua.os.family} - "
            f"{ua.browser.family}"
        )

        device, created = (
            UserDevice.objects.get_or_create(

                user=user,

                ip_address=ip_address,

                user_agent=user_agent_string,

                defaults={

                    'device_name': device_name,

                    'device_type': (
                        'Mobile'
                        if ua.is_mobile
                        else 'Desktop'
                    ),

                    'browser': ua.browser.family,
                }
            )
        )

        return device