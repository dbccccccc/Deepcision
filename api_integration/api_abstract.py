"""
Abstract Base Class Definition for API Integration Layer
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class APIBase(ABC):
    """Abstract Base Class for API Interface"""
    
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.base_url: Optional[str] = kwargs.get('base_url')
        self.timeout: int = kwargs.get('timeout', 30)
        self.headers: Dict[str, str] = self._build_headers()
    
    @abstractmethod
    def _build_headers(self) -> Dict[str, str]:
        """Build API Request Headers"""
        pass
    
    @abstractmethod
    async def call_api(self, endpoint: str, method: str = 'GET', 
                      data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call API Endpoint"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check API Service Health Status"""
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

class DeepSeekAPI(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def query(self, prompt: str, max_tokens=2000) -> str:
        # Implement DeepSeek specific call logic
        # Use requests library for API calls
        pass
    
    def format_response(self, raw_response: dict) -> str:
        # Extract and format DeepSeek response
        return raw_response['choices'][0]['text']

# Other API implementations follow similar structure... 