# securitydev/namespaces/async_ip_intel.py (Async Methods)
import httpx

# Import from parent/sibling modules
from ..models.ip_intel import GeoIpLookupData, ReputationData

# No need to import SecurityDevApiError directly here if only raised via base method
from .base import BaseNamespace  # Import the base class


class AsyncIpIntelNamespace(BaseNamespace):  # Inherit from BaseNamespace
    """Groups asynchronous IP Intel related API calls."""

    # __init__ still needs the *specific* client type for its methods
    def __init__(self, client: httpx.AsyncClient):
        # Call the base class initializer (optional if base __init__ does little)
        super().__init__(client)
        # Store the specifically typed client for use in this class's methods
        self._async_client = (
            client  # Use a different name or cast self._client if needed
        )

    # _handle_api_error is now inherited from BaseNamespace - REMOVE IT FROM HERE

    async def geolocate(self, ip_address: str) -> GeoIpLookupData:
        """
        (Async) Lookup GeoIP information for a single IP address.
        """
        url = f"/v1/ip-intel/geolocate/{ip_address}"
        try:
            # Use the specifically stored async client
            response = await self._async_client.get(url)
            response.raise_for_status()
            return GeoIpLookupData.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            # Call the inherited error handler
            raise self._handle_api_error(e) from None

    async def reputation(self, ip_address: str) -> ReputationData:
        """
        (Async) Lookup reputation information for a single IP address.
        """
        url = f"/v1/ip-intel/reputation/{ip_address}"
        try:
            # Use the specifically stored async client
            response = await self._async_client.get(url)
            response.raise_for_status()
            return ReputationData.model_validate(response.json())
        except httpx.HTTPStatusError as e:
            # Call the inherited error handler
            raise self._handle_api_error(e) from None
