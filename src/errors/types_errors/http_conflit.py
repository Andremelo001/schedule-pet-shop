class HttpConflitError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = 'Conflit'
        self.status_code = 409