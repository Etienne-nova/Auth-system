from rest_framework.views import exception_handler

from apps.authentication.utils.api_response import (
    ApiResponse
)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        response.data = ApiResponse.error(

            message=response.data.get(
                'detail',
                'Validation error'
            ),

            errors=response.data
        )

    return response