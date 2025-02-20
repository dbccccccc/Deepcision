"""
DeepSeek Tokenizer Implementation

This module implements the tokenizer for DeepSeek models using HuggingFace transformers.
"""

import os
from typing import List
from transformers import AutoTokenizer
from .tokenizer_base import TokenizerBase


class DeepSeekTokenizer(TokenizerBase):
    """DeepSeek tokenizer implementation"""
    
    def __init__(self, model_dir: str = None):
        """
        Initialize DeepSeek tokenizer
        
        Args:
            model_dir: Directory containing tokenizer files, defaults to current directory
        """
        if model_dir is None:
            model_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_dir,
            trust_remote_code=True
        )
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token ids"""
        return self.tokenizer.encode(text)
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token ids back to text"""
        return self.tokenizer.decode(token_ids)
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text"""
        return len(self.encode(text))
    
    def get_vocab_size(self) -> int:
        """Get the size of vocabulary"""
        return self.tokenizer.vocab_size
    
    def get_model_max_length(self) -> int:
        """Get maximum sequence length supported by the model"""
        return self.tokenizer.model_max_length
