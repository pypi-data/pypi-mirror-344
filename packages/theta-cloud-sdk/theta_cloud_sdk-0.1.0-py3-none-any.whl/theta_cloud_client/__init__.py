"""A client library for accessing theta-cloud"""

from .client import AuthenticatedClient, Client
from .browser_manager import BrowserManager

__all__ = (
    "AuthenticatedClient",
    "Client",
    "BrowserManager",
)
