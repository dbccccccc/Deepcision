"""
API Integration Package

This package handles all API integrations and their configurations.
"""

import os
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenRouterError(Exception):
    """Base exception class for OpenRouter API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 error_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.error_data = error_data or {}
        super().__init__(self.message)

class ConfigurationError(OpenRouterError):
    """Raised when there are configuration issues"""
    pass

class AuthenticationError(OpenRouterError):
    """Raised when there are authentication issues"""
    pass

class APIError(OpenRouterError):
    """Raised when the API returns an error"""
    pass

class NetworkError(OpenRouterError):
    """Raised when there are network connectivity issues"""
    pass

class ResponseError(OpenRouterError):
    """Raised when there are issues with response parsing"""
    pass

class HTTPStatus(Enum):
    """HTTP status codes used by OpenRouter API"""
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    REQUEST_TIMEOUT = 408
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

@dataclass
class OpenRouterResponse:
    """Standardized response structure"""
    content: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None
    finish_reason: Optional[str] = None

class OpenRouterConfig:
    """OpenRouter API configuration and constants"""
    
    # Base configuration
    BASE_URL: str = os.getenv("OPENROUTER_API_BASE_URL", "https://openrouter.ai/api/v1")
    API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    DEFAULT_TIMEOUT: int = int(os.getenv("OPENROUTER_API_TIMEOUT", "30"))
    
    # Default model settings
    DEFAULT_MODEL: str = os.getenv("OPENROUTER_DEFAULT_MODEL", "openai/gpt-4")
    DEFAULT_TEMPERATURE: float = float(os.getenv("OPENROUTER_DEFAULT_TEMPERATURE", "0.7"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("OPENROUTER_DEFAULT_MAX_TOKENS", "2000"))
    
    # Optional site information for rankings
    SITE_URL: Optional[str] = os.getenv("OPENROUTER_SITE_URL")
    SITE_NAME: Optional[str] = os.getenv("OPENROUTER_SITE_NAME")

    # Rate limiting settings
    MAX_RETRIES: int = int(os.getenv("OPENROUTER_MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("OPENROUTER_RETRY_DELAY", "1.0"))
    
    # Validation settings
    MIN_TEMPERATURE: float = 0.0
    MAX_TEMPERATURE: float = 2.0
    MIN_MAX_TOKENS: int = 1
    MAX_MAX_TOKENS: int = 32000  # This should be adjusted based on model limits

    @classmethod
    def validate_temperature(cls, temp: float) -> float:
        """Validate and clamp temperature value"""
        return max(min(temp, cls.MAX_TEMPERATURE), cls.MIN_TEMPERATURE)

    @classmethod
    def validate_max_tokens(cls, tokens: int) -> int:
        """Validate max_tokens value"""
        if not cls.MIN_MAX_TOKENS <= tokens <= cls.MAX_MAX_TOKENS:
            raise ConfigurationError(
                f"max_tokens must be between {cls.MIN_MAX_TOKENS} and {cls.MAX_MAX_TOKENS}")
        return tokens

    @classmethod
    def validate_api_key(cls, api_key: Optional[str]) -> str:
        """Validate API key"""
        if not api_key:
            raise ConfigurationError("OpenRouter API key not found")
        if not api_key.startswith(("sk-or-", "sk-")):
            raise ConfigurationError("Invalid OpenRouter API key format")
        return api_key

# Export commonly used classes
from .api_abstract import APIBase, ApiConfig
from .api_manager import ApiManager
from .openrouter_api import OpenRouterAPI, OpenRouterModel
