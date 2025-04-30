"""
securitydev - A modern Python client for the security.dev API.
Provides both synchronous (default) and asynchronous clients.
"""

__version__ = "1.0.0"

from .async_client import AsyncSecurityClient  # Async client
from .client import SecurityClient  # Default Sync client
from .exceptions import SecurityDevApiError, SecurityDevError
from .models import ip_intel  # Expose models namespace

# Make primary classes and exceptions easily accessible
__all__ = [
    "SecurityClient",  # Sync (Default)
    "AsyncSecurityClient",  # Async
    "SecurityDevError",
    "SecurityDevApiError",
    "ip_intel",  # Access models like securitydev.ip_intel.ReputationData
]
