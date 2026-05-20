"""Tally Prime connector - uses mock provider when USE_MOCK_DATA=true."""

from typing import Dict, Any, List, Optional

from app.integrations.base_connector import BaseConnector
from app.integrations.mock_providers.tally_mock import TallyMockProvider
from app.core.config import settings


class TallyConnector(BaseConnector):
    """Connector for Tally Prime integration."""

    def __init__(self, config: Dict[str, Any] = None, credentials: Dict[str, Any] = None):
        super().__init__(config, credentials)
        self._mock_provider = TallyMockProvider() if settings.USE_MOCK_DATA else None

    def platform_name(self) -> str:
        return "tally_prime"

    async def connect(self) -> bool:
        """Connect to Tally Prime (ODBC/XML or mock)."""
        if settings.USE_MOCK_DATA:
            self._connected = True
            return True

        # Real Tally connection via ODBC or XML would go here
        self._connected = True
        return True

    async def disconnect(self) -> bool:
        self._connected = False
        return True

    async def health_check(self) -> Dict[str, Any]:
        if settings.USE_MOCK_DATA:
            return {
                "healthy": True,
                "message": "Mock Tally Prime connection is active",
                "platform": "tally_prime",
                "mode": "mock",
            }
        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "platform": "tally_prime",
            "mode": "live",
        }

    async def fetch_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch sales vouchers from Tally as invoices."""
        if settings.USE_MOCK_DATA:
            vouchers = self._mock_provider.get_vouchers()
            return [v for v in vouchers if v["voucher_type"] == "Sales"]
        return []

    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch purchase vouchers from Tally as bills."""
        if settings.USE_MOCK_DATA:
            vouchers = self._mock_provider.get_vouchers()
            return [v for v in vouchers if v["voucher_type"] == "Purchase"]
        return []

    async def fetch_trial_balance(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_trial_balance()
        return {}

    async def fetch_ledgers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_ledgers()
        return []

    async def fetch_all_vouchers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch all voucher types from Tally."""
        if settings.USE_MOCK_DATA:
            return self._mock_provider.get_vouchers()
        return []
