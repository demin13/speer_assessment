class Validator:

    @staticmethod
    def TrimSerializerError(error):
        if isinstance(error, dict):
            for key, value in error.items():
                if isinstance(value, list):
                    return value[0]
        return error