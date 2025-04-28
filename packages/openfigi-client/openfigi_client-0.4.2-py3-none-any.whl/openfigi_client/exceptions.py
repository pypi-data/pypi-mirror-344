class OpenFigiError(Exception):
    """Base class for OpenFIGI exceptions."""


class HTTPError(OpenFigiError):
    """Raised when an HTTP error occurs."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP error {self.status_code}: {self.message}")


class TooManyMappingJobsError(OpenFigiError):
    """Raised when the number of mapping jobs exceeds the limit."""


class FilterQueryError(OpenFigiError):
    """Raised when a filter query is invalid."""
