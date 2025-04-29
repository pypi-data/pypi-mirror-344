class NotValidCfgError(Exception):
    """Exception raised when the configuration is not valid."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class AppError(Exception):
    """Exception raised for application errors."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
