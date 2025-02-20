"""
Tavily API Implementation

This module implements the Tavily API for web search and content extraction.
"""

import os
from typing import Dict, Any, List, Optional, Union
from enum import Enum
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SearchTopic(str, Enum):
    """Search topic options"""
    GENERAL = "general"
    NEWS = "news"

class SearchDepth(str, Enum):
    """Search depth options"""
    BASIC = "basic"
    ADVANCED = "advanced"

class TimeRange(str, Enum):
    """Time range options"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    D = "d"
    W = "w"
    M = "m"
    Y = "y"

class ExtractDepth(str, Enum):
    """Extract depth options"""
    BASIC = "basic"
    ADVANCED = "advanced"

class TavilyAPI:
    """Tavily API implementation"""

    BASE_URL = "https://api.tavily.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily API client
        
        Args:
            api_key: Tavily API key, defaults to TAVILY_API_KEY environment variable
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("Tavily API key not found")

    def _build_headers(self) -> Dict[str, str]:
        """Build API request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _call_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request to Tavily"""
        url = f"{self.BASE_URL}{endpoint}"
        
        async with aiohttp.ClientSession(headers=self._build_headers()) as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    
                    error_data = await response.json()
                    raise Exception(f"API call failed: {response.status} - {error_data}")
            except aiohttp.ClientError as e:
                raise Exception(f"Network request failed: {str(e)}")

    async def search(self,
                    query: str,
                    topic: Union[str, SearchTopic] = SearchTopic.GENERAL,
                    search_depth: Union[str, SearchDepth] = SearchDepth.BASIC,
                    max_results: int = 5,
                    time_range: Optional[Union[str, TimeRange]] = None,
                    days: Optional[int] = None,
                    include_answer: bool = False,
                    include_raw_content: bool = False,
                    include_images: bool = False,
                    include_image_descriptions: bool = False,
                    include_domains: Optional[List[str]] = None,
                    exclude_domains: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute a search query using Tavily Search
        
        Args:
            query: Search query to execute
            topic: Category of the search (general/news)
            search_depth: Depth of search (basic/advanced)
            max_results: Maximum number of results (1-20)
            time_range: Time range filter
            days: Number of days back for news
            include_answer: Include LLM-generated answer
            include_raw_content: Include parsed HTML content
            include_images: Include image search results
            include_image_descriptions: Include image descriptions
            include_domains: Domains to include
            exclude_domains: Domains to exclude
            
        Returns:
            Search results including query, answer, images and results
        """
        if not 0 < max_results < 20:
            raise ValueError("max_results must be between 1 and 19")
            
        if days is not None and days <= 0:
            raise ValueError("days must be greater than 0")

        data = {
            "query": query,
            "topic": topic if isinstance(topic, str) else topic.value,
            "search_depth": search_depth if isinstance(search_depth, str) else search_depth.value,
            "max_results": max_results,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "include_images": include_images,
            "include_image_descriptions": include_image_descriptions
        }

        if time_range:
            data["time_range"] = time_range if isinstance(time_range, str) else time_range.value
        if days:
            data["days"] = days
        if include_domains:
            data["include_domains"] = include_domains
        if exclude_domains:
            data["exclude_domains"] = exclude_domains

        return await self._call_api("/search", data)

    async def extract(self,
                     urls: Union[str, List[str]],
                     include_images: bool = False,
                     extract_depth: Union[str, ExtractDepth] = ExtractDepth.BASIC) -> Dict[str, Any]:
        """
        Extract web page content from URLs
        
        Args:
            urls: Single URL or list of URLs to extract content from
            include_images: Include list of extracted images
            extract_depth: Depth of extraction process
            
        Returns:
            Extracted content including raw content and images
        """
        if isinstance(urls, str):
            urls = [urls]

        data = {
            "urls": urls,
            "include_images": include_images,
            "extract_depth": extract_depth if isinstance(extract_depth, str) else extract_depth.value
        }

        return await self._call_api("/extract", data) 