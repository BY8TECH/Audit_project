"""Zoho Books connector - uses mock provider when USE_MOCK_DATA=true."""

from typing import Dict, Any, List, Optional

from app.integrations.base_connector import BaseConnector
from app.integrations.mock_providers.zoho_mock import ZohoMockProvider
from app.core.config import settings


class ZohoConnector(BaseConnector):
    """Connector for Zoho Books integration."""

    def __init__(self, config: Dict[str, Any] = None, credentials: Dict[str, Any] = None):
        super().__init__(config, credentials)
        self._mock_provider = ZohoMockProvider() if settings.USE_MOCK_DATA else None

    def platform_name(self) -> str:
        return "zoho_books"

    async def connect(self) -> bool:
        """Connect to Zoho Books API (or mock)."""
        if settings.USE_MOCK_DATA:
            self._connected = True
            return True

        # Real API connection would go here
        # client_id = self.credentials.get("client_id")
        # client_secret = self.credentials.get("client_secret")
        # ...
        self._connected = True
        return True

    async def disconnect(self) -> bool:
        """Disconnect from Zoho Books."""
        self._connected = False
        return True

    async def health_check(self) -> Dict[str, Any]:
        """Check Zoho Books connection health."""
        if settings.USE_MOCK_DATA:
            return {
                "healthy": True,
                "message": "Mock Zoho Books connection is active",
                "platform": "zoho_books",
                "mode": "mock",
            }

        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "platform": "zoho_books",
            "mode": "live",
        }

    async def fetch_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch invoices from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_invoices()

        # Real API call would go here
        return []

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch bills from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_bills()

        return []

    async def fetch_trial_balance(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fetch trial balance from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_trial_balance()

        return {}

    async def fetch_ledgers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch chart of accounts from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_chart_of_accounts()

        return []
