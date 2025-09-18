class BusinessError(Exception):
    def __init__(self, message: str):
        self.message = message
        # self.error = error
        super().__init__(message)


class ValidationError(BusinessError):
    pass

