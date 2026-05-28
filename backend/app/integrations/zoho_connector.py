"""Zoho Books connector - uses mock provider when USE_MOCK_DATA=true."""

from typing import Dict, Any, List, Optional
import httpx

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

        self.access_token = self.credentials.get("api_key")
        self.org_id = self.credentials.get("org_id")
        
        if not self.access_token or not self.org_id:
            raise ValueError("Missing Access Token (in API Key field) or Organization ID")

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

        url = "https://www.zohoapis.in/books/v3/invoices"
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        query_params = {"organization_id": self.org_id}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            data = response.json()
            return data.get("invoices", [])

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch bills from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_bills()

        url = "https://www.zohoapis.in/books/v3/bills"
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        query_params = {"organization_id": self.org_id}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            data = response.json()
            return data.get("bills", [])

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
