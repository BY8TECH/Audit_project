"""Income Tax Portal connector - uses mock provider when USE_MOCK_DATA=true."""

from typing import Dict, Any, List, Optional

from app.integrations.base_connector import BaseConnector
from app.integrations.mock_providers.income_tax_mock import IncomeTaxMockProvider
from app.core.config import settings


class IncomeTaxConnector(BaseConnector):
    """Connector for Income Tax Portal integration."""

    def __init__(self, config: Dict[str, Any] = None, credentials: Dict[str, Any] = None):
        super().__init__(config, credentials)
        self._mock_provider = IncomeTaxMockProvider() if settings.USE_MOCK_DATA else None

    def platform_name(self) -> str:
        return "income_tax"

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
                "message": "Mock Income Tax Portal connection is active",
                "platform": "income_tax",
                "mode": "mock",
            }
        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "platform": "income_tax",
            "mode": "live",
        }

    async def fetch_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Not applicable to Income Tax."""
        return []

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Not applicable to Income Tax."""
        return []

    async def fetch_trial_balance(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Not applicable to Income Tax."""
        return {}

    async def fetch_ledgers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Not applicable to Income Tax."""
        return []

    async def fetch_pan_records(self) -> List[Dict[str, Any]]:
        """Fetch all PAN records."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_pan_records()
        return []

    async def verify_pan(self, pan: str) -> Dict[str, Any]:
        """Verify a PAN number."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.verify_pan(pan)
        return {"valid": False, "message": "Live API not configured"}

    async def fetch_filing_status(self, pan: str) -> Dict[str, Any]:
        """Fetch ITR filing status."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_filing_status(pan)
        return {}

    async def fetch_tds_summary(self, pan: str) -> Dict[str, Any]:
        """Fetch TDS summary."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_tds_summary(pan)
        return {}
