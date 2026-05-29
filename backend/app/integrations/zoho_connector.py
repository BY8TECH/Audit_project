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

        self.refresh_token = self.credentials.get("refresh_token")
        self.org_id = self.credentials.get("org_id")
        self.location = self.credentials.get("location", "in")
        
        if not self.refresh_token or not self.org_id:
            raise ValueError("Missing Refresh Token or Organization ID")

        # Automatically fetch initial access token
        await self._refresh_access_token()

        self._connected = True
        return True

    async def _refresh_access_token(self):
        """Fetch a new access token using the refresh token."""
        url = f"https://accounts.zoho.{self.location}/oauth/v2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": settings.ZOHO_CLIENT_ID,
            "client_secret": settings.ZOHO_CLIENT_SECRET
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            if response.status_code != 200:
                self._connected = False
                raise ValueError(f"Failed to refresh access token: {response.text}")
            
            json_data = response.json()
            if "error" in json_data:
                self._connected = False
                raise ValueError(f"Zoho error refreshing token: {json_data['error']}")
                
            self.access_token = json_data.get("access_token")
            self._connected = True

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

        await self._refresh_access_token()
        url = f"https://www.zohoapis.{self.location}/books/v3/invoices"
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        all_invoices = []
        page = 1
        has_more_page = True
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            while has_more_page:
                query_params = {"organization_id": self.org_id, "page": page, "per_page": 200}
                response = await client.get(url, headers=headers, params=query_params)
                response.raise_for_status()
                data = response.json()
                all_invoices.extend(data.get("invoices", []))
                
                page_context = data.get("page_context", {})
                has_more_page = page_context.get("has_more_page", False)
                page += 1
                
        return all_invoices

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch bills from Zoho Books."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_bills()

        await self._refresh_access_token()
        url = f"https://www.zohoapis.{self.location}/books/v3/bills"
        headers = {"Authorization": f"Zoho-oauthtoken {self.access_token}"}
        all_bills = []
        page = 1
        has_more_page = True
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            while has_more_page:
                query_params = {"organization_id": self.org_id, "page": page, "per_page": 200}
                response = await client.get(url, headers=headers, params=query_params)
                response.raise_for_status()
                data = response.json()
                all_bills.extend(data.get("bills", []))
                
                page_context = data.get("page_context", {})
                has_more_page = page_context.get("has_more_page", False)
                page += 1
                
        return all_bills

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
