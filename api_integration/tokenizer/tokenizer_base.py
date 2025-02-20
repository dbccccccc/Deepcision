"""
Base Tokenizer Interface

This module defines the base interface for all tokenizer implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union


class TokenizerBase(ABC):
    """Base class for all tokenizer implementations"""
    
    @abstractmethod
    def encode(self, text: str) -> List[int]:
        """
        Encode text to token ids
        
        Args:
            text: Input text to encode
            
        Returns:
            List of token ids
        """
        pass
    
    @abstractmethod
    def decode(self, token_ids: List[int]) -> str:
        """
        Decode token ids back to text
        
        Args:
            token_ids: List of token ids to decode
            
        Returns:
            Decoded text
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text
        
        Args:
            text: Input text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass
    
    @abstractmethod
    def get_vocab_size(self) -> int:
        """
        Get the size of vocabulary
        
        Returns:
            Size of vocabulary
        """
        pass
    
    @abstractmethod
    def get_model_max_length(self) -> int:
        """
        Get maximum sequence length supported by the model
        
        Returns:
            Maximum sequence length
        """
        pass 