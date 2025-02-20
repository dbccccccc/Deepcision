"""
Tokenizer Package

This package provides tokenizer implementations and services for text tokenization.
"""

from .tokenizer_base import TokenizerBase
from .deepseek_tokenizer import DeepSeekTokenizer
from .tokenizer_service import TokenizerService

# Create a default tokenizer service instance
_default_service = TokenizerService()

def get_tokenizer(name: str, model_dir: str = None) -> TokenizerBase:
    """
    Get a tokenizer instance by name
    
    Args:
        name: Name of the tokenizer
        model_dir: Optional directory containing tokenizer files
        
    Returns:
        TokenizerBase: Tokenizer instance
    """
    return _default_service.get_tokenizer(name, model_dir)

def register_tokenizer(name: str, tokenizer_class: type):
    """
    Register a new tokenizer class
    
    Args:
        name: Name for the tokenizer
        tokenizer_class: TokenizerBase implementation class
    """
    _default_service.register_tokenizer(name, tokenizer_class)

# Export commonly used classes and functions
__all__ = [
    'TokenizerBase',
    'DeepSeekTokenizer',
    'TokenizerService',
    'get_tokenizer',
    'register_tokenizer'
] 