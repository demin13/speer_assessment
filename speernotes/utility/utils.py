import traceback
from rest_framework.response import Response
from rest_framework import status

class Validator:

    @staticmethod
    def TrimSerializerError(error):
        if isinstance(error, dict):
            for key, value in error.items():
                if isinstance(value, list):
                    return value[0]
        return error
    
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)

            return Response(
                data={"message": f"Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper
