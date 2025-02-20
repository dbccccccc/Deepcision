"""
Tokenizer Service

This module provides a centralized service for managing and using different tokenizer implementations.
"""

from typing import Dict, Optional, Type
from .tokenizer_base import TokenizerBase
from .deepseek_tokenizer import DeepSeekTokenizer


class TokenizerService:
    """Service class for managing tokenizers"""
    
    def __init__(self):
        self._tokenizers: Dict[str, TokenizerBase] = {}
        self._tokenizer_classes: Dict[str, Type[TokenizerBase]] = {
            "deepseek": DeepSeekTokenizer
        }
    
    def get_tokenizer(self, name: str, model_dir: Optional[str] = None) -> TokenizerBase:
        """
        Get a tokenizer instance by name
        
        Args:
            name: Name of the tokenizer
            model_dir: Optional directory containing tokenizer files
            
        Returns:
            TokenizerBase: Tokenizer instance
            
        Raises:
            ValueError: If tokenizer name is not supported
        """
        if name not in self._tokenizer_classes:
            raise ValueError(f"Unsupported tokenizer: {name}")
            
        if name not in self._tokenizers:
            tokenizer_class = self._tokenizer_classes[name]
            self._tokenizers[name] = tokenizer_class(model_dir)
            
        return self._tokenizers[name]
    
    def register_tokenizer(self, name: str, tokenizer_class: Type[TokenizerBase]):
        """
        Register a new tokenizer class
        
        Args:
            name: Name for the tokenizer
            tokenizer_class: TokenizerBase implementation class
        """
        self._tokenizer_classes[name] = tokenizer_class 