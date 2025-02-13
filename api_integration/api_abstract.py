"""
Abstract Base Class Definition for API Integration Layer

This module defines the core interfaces and data structures for API integrations.
It provides abstract base classes that all specific API implementations must follow,
ensuring consistent behavior across different API providers.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

from agents.role_manager import Agent


@dataclass
class ApiConfig:
    """
    Configuration data class for API settings
    
    Attributes:
        base_url (Optional[str]): Base URL for API endpoints
        api_key (Optional[str]): Authentication key for API access
        model (Optional[str]): Model identifier for AI services
        timeout (Optional[int]): Request timeout in seconds
    """
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    timeout: Optional[int] = None


class APIBase(ABC):
    """
    Abstract Base Class for API Interface
    
    This class defines the core interface that all API implementations must follow.
    It provides basic structure for API authentication, request handling, and
    standardized communication methods.
    
    Attributes:
        config (ApiConfig): Configuration settings for the API
        api_name (str): Unique identifier for the API implementation
        headers (Dict[str, str]): HTTP headers for API requests
    """
    config: ApiConfig
    api_name: str
    headers: Dict[str, str]

    def __init__(self, api_name: str, config: ApiConfig):
        """
        Initialize API interface with configuration
        
        Args:
            api_name (str): Unique identifier for this API implementation
            config (ApiConfig): Configuration settings for the API
        """
        self.api_name = api_name
        self.config = config
        self.headers = self._build_headers()

    @abstractmethod
    def _build_headers(self) -> Dict[str, str]:
        """
        Build API Request Headers
        
        Returns:
            Dict[str, str]: Dictionary of HTTP headers required for API requests
        """
        pass

    @abstractmethod
    async def call_api(self,
                       endpoint: str, method: str = 'GET',
                       data: Optional[Dict[str, Any]] = None
                       ) -> Dict[str, Any]:
        """
        Call API Endpoint
        
        Args:
            endpoint (str): API endpoint path
            method (str): HTTP method (GET, POST, etc.)
            data (Optional[Dict[str, Any]]): Request payload data
            
        Returns:
            Dict[str, Any]: API response data
            
        Raises:
            Exception: If API call fails or returns error
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check API Service Health Status
        
        Returns:
            bool: True if API service is healthy and accessible
        """
        pass

    @abstractmethod
    async def chat(self, prompt: str, role: Agent, **kwargs) -> str:
        """
        Unified Chat Interface for AI Models
        
        Args:
            prompt (str): User input/prompt
            role (Agent): Agent configuration for context
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: Generated response from the AI model
        """
        pass


class BaseAIProvider(ABC):
    """
    Abstract Base Class for AI Service Providers
    
    This class defines the interface for AI-specific functionality,
    particularly focused on query-response interactions.
    """
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> str:
        """
        Unified Query Interface
        
        Provides a synchronous interface for querying AI models.
        
        Args:
            prompt (str): Input text/prompt
            **kwargs: Additional model-specific parameters
            
        Returns:
            str: Generated response from the AI model
        """
        pass

    @abstractmethod
    def format_response(self, raw_response: dict) -> str:
        """
        Unified Response Formatting
        
        Standardizes the formatting of raw API responses into clean text output.
        
        Args:
            raw_response (dict): Raw API response data
            
        Returns:
            str: Formatted text response
            
        Raises:
            Exception: If response format is invalid or unexpected
        """
        pass
