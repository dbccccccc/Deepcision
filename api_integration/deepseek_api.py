"""
DeepSeek API Integration Implementation
Supports both deepseek-chat and deepseek-reasoner models
"""
import json
import os
from typing import Dict, Any, Optional, List, Union
import aiohttp
from dotenv import load_dotenv
from .api_abstract import APIBase, BaseAIProvider

# Load environment variables
load_dotenv()

class DeepSeekAPI(APIBase, BaseAIProvider):
    """DeepSeek API Implementation Class"""
    
    BASE_URL = os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        self.model: str = kwargs.pop('model', 'deepseek-chat')  # Default to chat model
        
        # Use provided API key first, otherwise use environment variable
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DeepSeek API key not found, please set DEEPSEEK_API_KEY in environment variables or pass it directly")
        
        # Get default parameters from environment variables
        default_timeout = int(os.getenv("DEEPSEEK_API_TIMEOUT", "30"))
        
        super().__init__(
            api_key=api_key,
            base_url=self.BASE_URL,
            timeout=kwargs.pop('timeout', default_timeout),
            **kwargs
        )
        
        # Load default parameters based on model type
        self.default_temperature = float(os.getenv(
            f"DEEPSEEK_{self.model.upper()}_TEMPERATURE",
            "0.7" if self.model == "deepseek-chat" else "0.3"
        ))
        self.default_max_tokens = int(os.getenv(
            f"DEEPSEEK_{self.model.upper()}_MAX_TOKENS",
            "2000" if self.model == "deepseek-chat" else "1500"
        ))
    
    def _build_headers(self) -> Dict[str, str]:
        """Build API request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def call_api(self, endpoint: str, method: str = 'POST', 
                      data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call DeepSeek API"""
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.request(method, url, json=data, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.json()
                    
                    error_data = await response.json()
                    raise Exception(f"API call failed: {response.status} - {error_data.get('error', 'Unknown error')}")
            except aiohttp.ClientError as e:
                raise Exception(f"Network request failed: {str(e)}")
    
    async def chat_completion(self, 
                            messages: List[Dict[str, str]], 
                            temperature: Optional[float] = None,
                            max_tokens: Optional[int] = None,
                            stream: bool = False,
                            **kwargs) -> Union[Dict[str, Any], aiohttp.ClientResponse]:
        """
        Call chat completion API
        
        Args:
            messages: List of conversation messages
            temperature: Sampling temperature, range 0-2
            max_tokens: Maximum number of tokens to generate
            stream: Whether to use streaming output
            **kwargs: Additional parameters
        """
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": min(max(temperature or self.default_temperature, 0), 2),
            "stream": stream
        }
        
        if max_tokens is not None:
            data["max_tokens"] = max_tokens
        elif self.default_max_tokens:
            data["max_tokens"] = self.default_max_tokens
            
        # Add optional parameters
        data.update({k: v for k, v in kwargs.items() if v is not None})
        
        if stream:
            # Special handling for streaming output
            return await self._stream_response("/v1/chat/completions", data)
        else:
            return await self.call_api("/v1/chat/completions", "POST", data)
    
    async def _stream_response(self, endpoint: str, data: Dict[str, Any]) -> aiohttp.ClientResponse:
        """Handle streaming response"""
        url = f"{self.base_url}{endpoint}"
        session = aiohttp.ClientSession(headers=self.headers)
        try:
            response = await session.post(url, json=data, timeout=self.timeout)
            if response.status != 200:
                error_data = await response.json()
                raise Exception(f"API call failed: {response.status} - {error_data.get('error', 'Unknown error')}")
            return response
        except Exception as e:
            await session.close()
            raise e
    
    async def health_check(self) -> bool:
        """Check API service health status"""
        try:
            # Call balance query endpoint to check service status
            await self.call_api("/v1/user/balance", "GET")
            return True
        except Exception:
            return False
    
    def query(self, prompt: str, **kwargs) -> str:
        """Implement unified query interface from BaseAIProvider"""
        # Implement synchronous version of query
        import asyncio
        messages = [{"role": "user", "content": prompt}]
        response = asyncio.run(self.chat_completion(messages, **kwargs))
        return self.format_response(response)
    
    def format_response(self, raw_response: dict) -> str:
        """Format API response"""
        try:
            return raw_response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise Exception("Invalid response format") 