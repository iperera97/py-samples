class RepositoryError(Exception):
    """Raised when repository layer fails (query, connection, retry exhaustion)."""
    def __init__(self, message: str, *, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause
