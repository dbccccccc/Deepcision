"""
Unit Tests for Tavily API Implementation
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from ..tavily_api import (
    TavilyAPI,
    SearchTopic,
    SearchDepth,
    TimeRange,
    ExtractDepth
)


class TestTavilyAPI(unittest.TestCase):
    """Test cases for TavilyAPI"""

    def setUp(self):
        """Set up test environment"""
        self.api_key = "test-api-key"
        self.api = TavilyAPI(self.api_key)

    def test_init_with_env_var(self):
        """Test initialization with environment variable"""
        with patch.dict(os.environ, {"TAVILY_API_KEY": "env-api-key"}):
            api = TavilyAPI()
            self.assertEqual(api.api_key, "env-api-key")

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, clear=True):
            with self.assertRaises(ValueError):
                TavilyAPI()

    def test_build_headers(self):
        """Test header building"""
        headers = self.api._build_headers()
        self.assertEqual(headers["Authorization"], f"Bearer {self.api_key}")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("aiohttp.ClientSession")
    async def test_search_basic(self, mock_session):
        """Test basic search functionality"""
        # Mock response
        mock_response = {
            "query": "test query",
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://test.com",
                    "content": "Test content"
                }
            ]
        }
        
        # Setup mock
        mock_context = MagicMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = MagicMock(
            return_value=mock_response
        )
        mock_session.return_value.post.return_value = mock_context

        # Test search
        result = await self.api.search("test query")
        
        # Verify request
        mock_session.return_value.post.assert_called_once()
        call_args = mock_session.return_value.post.call_args
        self.assertEqual(call_args[0][0], f"{TavilyAPI.BASE_URL}/search")
        
        # Verify request data
        request_data = json.loads(call_args[1]["json"])
        self.assertEqual(request_data["query"], "test query")
        self.assertEqual(request_data["topic"], SearchTopic.GENERAL.value)
        self.assertEqual(request_data["search_depth"], SearchDepth.BASIC.value)
        
        # Verify response
        self.assertEqual(result, mock_response)

    @patch("aiohttp.ClientSession")
    async def test_search_advanced(self, mock_session):
        """Test advanced search functionality"""
        mock_response = {"status": "success"}
        mock_context = MagicMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = MagicMock(
            return_value=mock_response
        )
        mock_session.return_value.post.return_value = mock_context

        result = await self.api.search(
            query="test query",
            topic=SearchTopic.NEWS,
            search_depth=SearchDepth.ADVANCED,
            max_results=10,
            time_range=TimeRange.WEEK,
            days=7,
            include_answer=True,
            include_images=True
        )

        # Verify request data
        call_args = mock_session.return_value.post.call_args
        request_data = json.loads(call_args[1]["json"])
        self.assertEqual(request_data["topic"], SearchTopic.NEWS.value)
        self.assertEqual(request_data["search_depth"], SearchDepth.ADVANCED.value)
        self.assertEqual(request_data["max_results"], 10)
        self.assertEqual(request_data["time_range"], TimeRange.WEEK.value)
        self.assertEqual(request_data["days"], 7)
        self.assertTrue(request_data["include_answer"])
        self.assertTrue(request_data["include_images"])

    @patch("aiohttp.ClientSession")
    async def test_search_validation(self, mock_session):
        """Test search parameter validation"""
        with self.assertRaises(ValueError):
            await self.api.search("test", max_results=0)
        
        with self.assertRaises(ValueError):
            await self.api.search("test", max_results=20)
            
        with self.assertRaises(ValueError):
            await self.api.search("test", days=0)

    @patch("aiohttp.ClientSession")
    async def test_extract_single_url(self, mock_session):
        """Test content extraction for single URL"""
        mock_response = {
            "results": [{
                "url": "https://test.com",
                "raw_content": "Test content"
            }]
        }
        
        mock_context = MagicMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = MagicMock(
            return_value=mock_response
        )
        mock_session.return_value.post.return_value = mock_context

        result = await self.api.extract("https://test.com")
        
        # Verify request
        call_args = mock_session.return_value.post.call_args
        request_data = json.loads(call_args[1]["json"])
        self.assertEqual(request_data["urls"], ["https://test.com"])
        self.assertEqual(request_data["extract_depth"], ExtractDepth.BASIC.value)
        
        # Verify response
        self.assertEqual(result, mock_response)

    @patch("aiohttp.ClientSession")
    async def test_extract_multiple_urls(self, mock_session):
        """Test content extraction for multiple URLs"""
        urls = ["https://test1.com", "https://test2.com"]
        mock_response = {
            "results": [
                {"url": url, "raw_content": f"Content from {url}"}
                for url in urls
            ]
        }
        
        mock_context = MagicMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = MagicMock(
            return_value=mock_response
        )
        mock_session.return_value.post.return_value = mock_context

        result = await self.api.extract(
            urls,
            include_images=True,
            extract_depth=ExtractDepth.ADVANCED
        )
        
        # Verify request
        call_args = mock_session.return_value.post.call_args
        request_data = json.loads(call_args[1]["json"])
        self.assertEqual(request_data["urls"], urls)
        self.assertTrue(request_data["include_images"])
        self.assertEqual(request_data["extract_depth"], ExtractDepth.ADVANCED.value)
        
        # Verify response
        self.assertEqual(result, mock_response)

    @patch("aiohttp.ClientSession")
    async def test_api_error_handling(self, mock_session):
        """Test API error handling"""
        mock_context = MagicMock()
        mock_context.__aenter__.return_value.status = 400
        mock_context.__aenter__.return_value.json = MagicMock(
            return_value={"error": "Bad request"}
        )
        mock_session.return_value.post.return_value = mock_context

        with self.assertRaises(Exception) as context:
            await self.api.search("test query")
        
        self.assertIn("API call failed", str(context.exception))


if __name__ == "__main__":
    unittest.main() 