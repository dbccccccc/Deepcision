"""
Abstract Base Class Definition for API Integration Layer
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

from agents.role_manager import Agent


@dataclass
class ApiConfig:
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    timeout: Optional[int] = None


class APIBase(ABC):
    """Abstract Base Class for API Interface"""
    config: ApiConfig
    api_name: str
    headers: Dict[str, str]

    def __init__(self, api_name: str, config: ApiConfig):
        self.api_name = api_name
        self.config = config
        self.headers = self._build_headers()

    @abstractmethod
    def _build_headers(self) -> Dict[str, str]:
        """Build API Request Headers"""
        pass

    @abstractmethod
    async def call_api(self,
                       endpoint: str, method: str = 'GET',
                       data: Optional[Dict[str, Any]] = None
                       ) -> Dict[str, Any]:
        """Call API Endpoint"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check API Service Health Status"""
        pass

    @abstractmethod
    async def chat(self, prompt: str, role: Agent, **kwargs) -> str:
        """Unified Query Interface"""
        pass


class BaseAIProvider(ABC):
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str:
        """Unified Query Interface"""
        pass

    @abstractmethod
    def format_response(self, raw_response: dict) -> str:
        """Unified Response Formatting"""
        pass
