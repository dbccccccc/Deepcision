from tokenizer import Tokenizer, TokenizerError

def main():
    # Create a tokenizer instance (uses o200k_base encoding)
    tokenizer = Tokenizer()
    
    # Example text
    text = "Hello, this is a sample text to demonstrate the tokenizer API!"
    
    try:
        # Simple token counting
        token_count = tokenizer.count_tokens(text)
        print(f"Token count: {token_count}")
    except TokenizerError as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 