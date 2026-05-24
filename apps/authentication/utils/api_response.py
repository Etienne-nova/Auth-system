class ApiResponse:

    @staticmethod
    def success(
        message="Success",
        data=None,
        status_code=200
    ):

        return {

            "success": True,

            "version": "v1",

            "message": message,

            "data": data,
            
            "status_code": status_code
        }
    @staticmethod
    def error(
        message="Error",
        errors=None,
        status_code=400
    ):

        return {

            "success": False,

            "version": "v1",

            "message": message,

            "errors": errors,
            
            "status_code": status_code
        }