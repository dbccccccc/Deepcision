"""
OpenRouter API Integration Implementation

This module implements the OpenRouter API integration, supporting all OpenRouter features
including chat completions, tool calls, structured outputs, and more.
"""

import json
import asyncio
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import aiohttp

from .api_abstract import APIBase, ApiConfig, BaseAIProvider
from agents.role_manager import Agent
from . import (
    OpenRouterConfig as Config,
    OpenRouterResponse,
    OpenRouterError,
    ConfigurationError,
    AuthenticationError,
    APIError,
    NetworkError,
    ResponseError,
    HTTPStatus
)

class OpenRouterModel(str, Enum):
    """Commonly used OpenRouter models"""
    GPT4 = "openai/gpt-4"
    GPT4_TURBO = "openai/gpt-4-turbo"
    CLAUDE_3_OPUS = "anthropic/claude-3-opus"
    CLAUDE_3_SONNET = "anthropic/claude-3-sonnet"
    MIXTRAL = "mistralai/mixtral-8x7b-instruct"
    DEEPSEEK_CHAT = "deepseek/deepseek-chat"

@dataclass
class OpenRouterConfig(ApiConfig):
    """Extended configuration for OpenRouter API"""
    http_referer: Optional[str] = None  # Site URL for rankings
    x_title: Optional[str] = None  # Site title for rankings

class OpenRouterAPI(APIBase, BaseAIProvider):
    """OpenRouter API Implementation Class"""

    def __init__(self, config: OpenRouterConfig, api_name: str = "openrouter"):
        try:
            # Use provided config first, then fall back to environment variables
            self.model = config.model or Config.DEFAULT_MODEL
            self.api_key = Config.validate_api_key(config.api_key or Config.API_KEY)
            self.timeout = config.timeout or Config.DEFAULT_TIMEOUT
            self.base_url = config.base_url or Config.BASE_URL
            
            # Store ranking headers
            self.http_referer = config.http_referer or Config.SITE_URL
            self.x_title = config.x_title or Config.SITE_NAME

            super().__init__(api_name, config)
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize OpenRouter API: {str(e)}")

    def _build_headers(self) -> Dict[str, str]:
        """Build API request headers"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add optional ranking headers
        if self.http_referer:
            headers["HTTP-Referer"] = self.http_referer
        if self.x_title:
            headers["X-Title"] = self.x_title
            
        return headers

    async def _handle_error_response(self, response: aiohttp.ClientResponse) -> None:
        """Handle error responses from the API"""
        try:
            error_data = await response.json()
        except:
            error_data = {"error": "Unknown error"}

        error_msg = error_data.get("error", {}).get("message", str(error_data))
        
        if response.status == HTTPStatus.UNAUTHORIZED.value:
            raise AuthenticationError("Invalid API key", response.status, error_data)
        elif response.status == HTTPStatus.PAYMENT_REQUIRED.value:
            raise APIError("Insufficient credits", response.status, error_data)
        elif response.status == HTTPStatus.TOO_MANY_REQUESTS.value:
            raise APIError("Rate limit exceeded", response.status, error_data)
        else:
            raise APIError(f"API request failed: {error_msg}", response.status, error_data)

    async def call_api(self, endpoint: str, method: str = 'POST',
                      data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call OpenRouter API with retry logic"""
        url = f"{self.base_url}{endpoint}"
        retries = Config.MAX_RETRIES
        
        while retries > 0:
            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.request(method, url, json=data, timeout=self.timeout) as response:
                        if response.status == HTTPStatus.OK.value:
                            return await response.json()
                        
                        # Handle rate limiting with retry
                        if response.status == HTTPStatus.TOO_MANY_REQUESTS.value:
                            retries -= 1
                            if retries > 0:
                                await asyncio.sleep(Config.RETRY_DELAY)
                                continue
                        
                        await self._handle_error_response(response)
                        
            except aiohttp.ClientError as e:
                raise NetworkError(f"Network request failed: {str(e)}")
            except asyncio.TimeoutError:
                raise NetworkError("Request timed out")
        
        raise APIError("Max retries exceeded")

    async def chat_completion(self,
                            messages: List[Dict[str, str]],
                            temperature: Optional[float] = None,
                            max_tokens: Optional[int] = None,
                            tools: Optional[List[Dict[str, Any]]] = None,
                            tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
                            response_format: Optional[Dict[str, str]] = None,
                            transforms: Optional[List[str]] = None,
                            models: Optional[List[str]] = None,
                            provider: Optional[Dict[str, Any]] = None,
                            **kwargs) -> Dict[str, Any]:
        """
        Call chat completion API with comprehensive OpenRouter features

        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            tools: List of tools available to the model
            tool_choice: Control which tool the model should use
            response_format: Force specific output format
            transforms: List of transforms to apply (e.g. ["middle-out"])
            models: List of model fallbacks
            provider: Provider routing preferences
            **kwargs: Additional parameters
        """
        try:
            # Validate input parameters
            if not messages:
                raise ConfigurationError("Messages cannot be empty")

            data = {
                "model": self.model,
                "messages": messages
            }

            # Add optional parameters with validation
            if temperature is not None:
                data["temperature"] = Config.validate_temperature(temperature)
            else:
                data["temperature"] = Config.DEFAULT_TEMPERATURE

            if max_tokens is not None:
                data["max_tokens"] = Config.validate_max_tokens(max_tokens)
            else:
                data["max_tokens"] = Config.DEFAULT_MAX_TOKENS

            # Add optional features
            if tools:
                data["tools"] = tools
            if tool_choice:
                data["tool_choice"] = tool_choice
            if response_format:
                data["response_format"] = response_format
            if transforms:
                data["transforms"] = transforms
            if models:
                data["models"] = models
            if provider:
                data["provider"] = provider

            # Add any remaining kwargs
            data.update({k: v for k, v in kwargs.items() if v is not None})

            response = await self.call_api("/chat/completions", "POST", data)
            return response

        except OpenRouterError:
            raise
        except Exception as e:
            raise APIError(f"Chat completion failed: {str(e)}")

    async def list_models(self) -> Dict[str, Any]:
        """Get list of available models"""
        return await self.call_api("/models", "GET")

    async def get_model_endpoints(self, author: str, slug: str) -> Dict[str, Any]:
        """Get endpoints for a specific model"""
        if not author or not slug:
            raise ConfigurationError("Author and slug are required")
        return await self.call_api(f"/models/{author}/{slug}/endpoints", "GET")

    async def get_credits(self) -> Dict[str, Any]:
        """Get account credits information"""
        return await self.call_api("/credits", "GET")

    async def health_check(self) -> bool:
        """Check API service health status"""
        try:
            await self.list_models()
            return True
        except Exception:
            return False

    def query(self, prompt: str, **kwargs) -> str:
        """Implement unified query interface from BaseAIProvider"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = asyncio.run(self.chat_completion(messages, **kwargs))
            return self.format_response(response)
        except Exception as e:
            raise APIError(f"Query failed: {str(e)}")

    def format_response(self, raw_response: dict) -> str:
        """Format API response"""
        try:
            return raw_response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise ResponseError(f"Invalid response format: {str(e)}")

    async def chat(self, prompt: str, role: Agent, **kwargs) -> str:
        """Implement chat interface with role-based context"""
        try:
            if not prompt or not role:
                raise ConfigurationError("Prompt and role are required")

            messages = [
                {
                    "role": "system",
                    "content": f"You are {role.role_config.name} {role.role_config.description}"
                },
                {
                    "role": "user",
                    "content": role.role_config.prompt_template.format(question=prompt)
                }
            ]
            
            response = await self.chat_completion(
                messages,
                temperature=role.role_config.temperature,
                max_tokens=role.role_config.max_tokens,
                **kwargs
            )
            
            return self.format_response(response)
        except OpenRouterError:
            raise
        except Exception as e:
            raise APIError(f"Chat failed: {str(e)}") 