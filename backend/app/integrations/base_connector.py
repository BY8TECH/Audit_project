"""Abstract base connector for all platform integrations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseConnector(ABC):
    """Abstract base class for platform connectors."""

    def __init__(self, config: Dict[str, Any] = None, credentials: Dict[str, Any] = None):
        self.config = config or {}
        self.credentials = credentials or {}
        self._connected = False

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the platform. Returns True if successful."""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the platform."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check if the connection is healthy.
        Returns dict with 'healthy' bool and 'message' string.
        """
        pass

    @abstractmethod
    async def fetch_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch invoices/sales data from the platform."""
        pass

    @abstractmethod
    async def fetch_bills(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch bills/purchase data from the platform."""
        pass

    @abstractmethod
    async def fetch_trial_balance(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fetch trial balance data."""
        pass

    @abstractmethod
    async def fetch_ledgers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch ledger/chart of accounts data."""
        pass

    @property
    def is_connected(self) -> bool:
        return self._connected

    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform identifier."""
        pass
