# securitydev/namespaces/base.py
"""Base class for API namespaces, providing common functionality."""

import http
from typing import Union  # To type hint the client

import httpx

# Need to import the exception from the parent directory's exceptions module
from ..exceptions import SecurityDevApiError


class BaseNamespace:
    """
    Base class for API namespaces.

    Handles common tasks like parsing API errors. Derived classes should
    implement the actual API call methods.
    """

    # Keep track of the client, could be sync or async
    # Use Union for type hinting, although runtime check might be needed
    # if behavior differs drastically (not the case for error handling here)
    def __init__(self, client: Union[httpx.Client, httpx.AsyncClient]):
        self._client = client  # Store the client if needed for future base methods

    def _handle_api_error(self, e: httpx.HTTPStatusError) -> SecurityDevApiError:
        """
        Parses an HTTPStatusError into a SecurityDevApiError, adding hints.

        This method is synchronous as it only inspects the exception object.
        """
        request_url = str(e.request.url)
        status_code = e.response.status_code

        # Determine base detail first
        base_detail = f"{status_code} {e.response.reason_phrase}"
        try:
            error_data = e.response.json()
            if isinstance(error_data, dict) and "detail" in error_data:
                api_detail = str(error_data["detail"]).strip()
                if api_detail:
                    base_detail = api_detail
        except Exception:
            # Ignore JSON parsing errors or missing 'detail'
            pass

        # Construct final detail, adding hint specifically for 403
        final_detail = base_detail
        if status_code == http.HTTPStatus.FORBIDDEN:  # Check specifically for 403
            final_detail += " (Please check if your API key is correct and active)"
        # Could add more hints for other common statuses here (e.g., 401, 429)

        return SecurityDevApiError(
            status_code=status_code,
            detail=final_detail,
            request_url=request_url,
        )
