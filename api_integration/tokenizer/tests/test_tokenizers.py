"""
Unit Tests for Tokenizer Implementations
"""

import os
import unittest
from typing import List
from ..tokenizer_base import TokenizerBase
from ..tokenizer_service import TokenizerService
from ..deepseek_tokenizer import DeepSeekTokenizer


class MockTokenizer(TokenizerBase):
    """Mock tokenizer for testing"""
    
    def encode(self, text: str) -> List[int]:
        return [1, 2, 3]  # Mock token ids
        
    def decode(self, token_ids: List[int]) -> str:
        return "mock text"  # Mock decoded text
        
    def count_tokens(self, text: str) -> int:
        return 3  # Mock token count
        
    def get_vocab_size(self) -> int:
        return 1000  # Mock vocab size
        
    def get_model_max_length(self) -> int:
        return 2048  # Mock max length


class TestTokenizerBase(unittest.TestCase):
    """Test cases for TokenizerBase interface"""
    
    def setUp(self):
        self.tokenizer = MockTokenizer()
    
    def test_encode(self):
        result = self.tokenizer.encode("test text")
        self.assertEqual(result, [1, 2, 3])
    
    def test_decode(self):
        result = self.tokenizer.decode([1, 2, 3])
        self.assertEqual(result, "mock text")
    
    def test_count_tokens(self):
        result = self.tokenizer.count_tokens("test text")
        self.assertEqual(result, 3)
    
    def test_get_vocab_size(self):
        result = self.tokenizer.get_vocab_size()
        self.assertEqual(result, 1000)
    
    def test_get_model_max_length(self):
        result = self.tokenizer.get_model_max_length()
        self.assertEqual(result, 2048)


class TestTokenizerService(unittest.TestCase):
    """Test cases for TokenizerService"""
    
    def setUp(self):
        self.service = TokenizerService()
    
    def test_register_tokenizer(self):
        self.service.register_tokenizer("mock", MockTokenizer)
        tokenizer = self.service.get_tokenizer("mock")
        self.assertIsInstance(tokenizer, MockTokenizer)
    
    def test_get_invalid_tokenizer(self):
        with self.assertRaises(ValueError):
            self.service.get_tokenizer("invalid")
    
    def test_tokenizer_singleton(self):
        tokenizer1 = self.service.get_tokenizer("mock")
        tokenizer2 = self.service.get_tokenizer("mock")
        self.assertIs(tokenizer1, tokenizer2)


@unittest.skipIf(not os.path.exists(os.path.join(os.path.dirname(__file__), "..", "tokenizer.json")),
                 "DeepSeek tokenizer files not found")
class TestDeepSeekTokenizer(unittest.TestCase):
    """Test cases for DeepSeekTokenizer"""
    
    def setUp(self):
        self.tokenizer = DeepSeekTokenizer()
    
    def test_encode_decode(self):
        text = "Hello, world!"
        tokens = self.tokenizer.encode(text)
        decoded = self.tokenizer.decode(tokens)
        self.assertIsInstance(tokens, list)
        self.assertIsInstance(decoded, str)
        self.assertTrue(len(tokens) > 0)
    
    def test_count_tokens(self):
        text = "Hello, world!"
        count = self.tokenizer.count_tokens(text)
        self.assertIsInstance(count, int)
        self.assertTrue(count > 0)
    
    def test_vocab_size(self):
        size = self.tokenizer.get_vocab_size()
        self.assertIsInstance(size, int)
        self.assertTrue(size > 0)
    
    def test_model_max_length(self):
        length = self.tokenizer.get_model_max_length()
        self.assertIsInstance(length, int)
        self.assertTrue(length > 0)


if __name__ == '__main__':
    unittest.main() 