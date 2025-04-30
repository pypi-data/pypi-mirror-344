from types import TracebackType
from typing import Optional, Type

import httpx

from .namespaces.async_ip_intel import AsyncIpIntelNamespace


class AsyncSecurityClient:
    """
    An **asynchronous** client for interacting with the security.dev API.

    Access specific API groups via namespaces (e.g., `client.ip_intel`).
    The default synchronous client is available as `SecurityClient`.

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

        # Core HTTPX client instance (Async)
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._auth_headers,
            timeout=self._timeout,
            follow_redirects=True,
        )

        # --- Initialize Namespaces ---
        # Pass the raw async httpx client to the namespace
        self.ip_intel = AsyncIpIntelNamespace(self._client)
        # In the future, add other async namespaces here:
        # self.user_intel = AsyncUserIntelNamespace(self._client)
        # self.email_intel = AsyncEmailIntelNamespace(self._client)

    async def close(self) -> None:
        """(Async) Closes the underlying HTTPX client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncSecurityClient":
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        """Exit the async context manager and close the client."""
        await self.close()

    # Note: Direct API call methods (like geolocate, reputation) are now removed
    # They reside within their respective namespace classes.
