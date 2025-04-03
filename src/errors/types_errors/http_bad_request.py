class HttpBadRequestError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'BabRequest'
        self.status_code = 400