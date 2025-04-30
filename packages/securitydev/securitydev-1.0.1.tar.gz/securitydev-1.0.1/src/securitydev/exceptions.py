# securitydev/exceptions.py
"""Custom exceptions for the securitydev library."""


class SecurityDevError(Exception):
    """Base exception class for securitydev errors."""

    pass


class SecurityDevApiError(SecurityDevError):
    """
    Exception raised when the security.dev API returns an error status (4xx or 5xx).

    Attributes:
        status_code (int): The HTTP status code returned by the API.
        detail (str): The error detail message provided by the API, or a
                      default message based on the status code.
        request_url (str): The URL that was requested.
    """

    def __init__(self, status_code: int, detail: str, request_url: str):
        self.status_code = status_code
        self.detail = detail
        self.request_url = request_url
        # Cleaner error message format
        super().__init__(
            f"API request to {request_url} failed with status {status_code}: {detail}"
        )
