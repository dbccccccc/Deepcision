import tiktoken

class TokenizerError(Exception):
    """Custom exception for tokenizer-related errors."""
    pass

class Tokenizer:
    """A class to handle text tokenization operations using o200k_base encoding"""
    
    ENCODING_NAME = "o200k_base"
    
    def __init__(self):
        """
        Initialize the tokenizer with o200k_base encoding
        
        Raises:
            TokenizerError: If the encoding initialization fails
        """
        try:
            self.encoding = tiktoken.get_encoding(self.ENCODING_NAME)
        except Exception as e:
            raise TokenizerError(f"Failed to initialize tokenizer: {str(e)}")

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string
        
        Args:
            text: The input text to tokenize
            
        Returns:
            int: Number of tokens
            
        Raises:
            TokenizerError: If tokenization fails
        """
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            raise TokenizerError(f"Failed to count tokens: {str(e)}")