"""GST Portal connector - uses mock provider when USE_MOCK_DATA=true."""

from typing import Dict, Any, List, Optional

from app.integrations.base_connector import BaseConnector
from app.integrations.mock_providers.gst_mock import GSTMockProvider
from app.core.config import settings


class GSTConnector(BaseConnector):
    """Connector for GST Portal integration."""

    def __init__(self, config: Dict[str, Any] = None, credentials: Dict[str, Any] = None):
        super().__init__(config, credentials)
        self._mock_provider = GSTMockProvider() if settings.USE_MOCK_DATA else None

    def platform_name(self) -> str:
        return "gst_portal"

    async def connect(self) -> bool:
        if settings.USE_MOCK_DATA:
            self._connected = True
            return True
        self._connected = True
        return True

    async def disconnect(self) -> bool:
        self._connected = False
        return True

    async def health_check(self) -> Dict[str, Any]:
        if settings.USE_MOCK_DATA:
            return {
                "healthy": True,
                "message": "Mock GST Portal connection is active",
                "platform": "gst_portal",
                "mode": "mock",
            }
        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "platform": "gst_portal",
            "mode": "live",
        }

    async def fetch_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch GSTR-1 data as invoice-level data."""
        if settings.USE_MOCK_DATA:
            gstr1 = self._mock_provider.get_gstr1_summary()
            return [gstr1]
        return []

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Not directly applicable to GST - returns empty."""
        return []

    async def fetch_trial_balance(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Not applicable to GST."""
        return {}

    async def fetch_ledgers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Not applicable to GST."""
        return []

    async def fetch_gstin_details(self) -> List[Dict[str, Any]]:
        """Fetch GSTIN records."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_gstin_records()
        return []

    async def fetch_gstr1_summary(self) -> Dict[str, Any]:
        """Fetch GSTR-1 summary."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_gstr1_summary()
        return {}

    async def fetch_gstr3b_summary(self) -> Dict[str, Any]:
        """Fetch GSTR-3B summary."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_gstr3b_summary()
        return {}

    async def fetch_filing_history(self) -> List[Dict[str, Any]]:
        """Fetch GST filing history."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_filing_history()
        return []

    async def verify_gstin(self, gstin: str) -> Dict[str, Any]:
        """Verify a GSTIN."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.verify_gstin(gstin)
        return {"valid": False, "message": "Live API not configured"}
