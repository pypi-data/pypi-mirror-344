from types import TracebackType
from typing import Optional, Type

import httpx

from .namespaces.ip_intel import IpIntelNamespace


class SecurityClient:
    """
    The default **synchronous** client for interacting with the security.dev API.

    Access specific API groups via namespaces (e.g., `client.ip_intel`).

    Args:
        key (str): Your security.dev API key (Bearer Token).
        base_url (str): The base URL for the security.dev API.
                        Defaults to "https://api.security.dev".
        timeout (float): Default timeout for HTTP requests in seconds.
                         Defaults to 5.0.
    """

    def __init__(
        self,
        key: str,
        base_url: str = "https://api.security.dev",
        timeout: float = 5.0,
    ):
        if not key:
            raise ValueError("API key 'key' cannot be empty.")

        self._base_url = base_url
        self._auth_headers = {"Authorization": f"Bearer {key}"}
        self._timeout = timeout

        # Core HTTPX client instance (Sync)
        self._client = httpx.Client(
            base_url=self._base_url,
            headers=self._auth_headers,
            timeout=self._timeout,
            follow_redirects=True,
        )

        # --- Initialize Namespaces ---
        # Pass the raw httpx client to the namespace
        self.ip_intel = IpIntelNamespace(self._client)
        # In the future, add other namespaces here:
        # self.user_intel = UserIntelNamespace(self._client)
        # self.email_intel = EmailIntelNamespace(self._client)

    def close(self) -> None:
        """(Sync) Closes the underlying HTTPX client."""
        self._client.close()

    def __enter__(self) -> "SecurityClient":
        """Enter the synchronous context manager."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        """Exit the synchronous context manager and close the client."""
        self.close()

    # Note: Direct API call methods (like geolocate, reputation) are now removed
    # They reside within their respective namespace classes.
