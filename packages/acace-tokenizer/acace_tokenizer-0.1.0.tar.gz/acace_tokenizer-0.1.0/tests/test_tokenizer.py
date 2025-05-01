"""
Tests for the acace_tokenizer module.
"""

import unittest
from acace_tokenizer import Tokenizer, tokenize_text


class TestTokenizer(unittest.TestCase):
    """Test cases for the Tokenizer class."""
    
    def test_simple_tokenization(self):
        """Test simple whitespace and punctuation-based tokenization."""
        text = "Hello, world! This is a test."
        tokenizer = Tokenizer(strategy="simple")
        tokens = tokenizer.tokenize(text)
        expected = ["Hello", ",", "world", "!", "This", "is", "a", "test", "."]
        self.assertEqual(tokens, expected)
    
    def test_case_preservation(self):
        """Test case preservation option."""
        text = "Hello WORLD"
        # With case preservation (default)
        tokenizer1 = Tokenizer(strategy="simple", preserve_case=True)
        tokens1 = tokenizer1.tokenize(text)
        self.assertEqual(tokens1, ["Hello", "WORLD"])
        
        # Without case preservation
        tokenizer2 = Tokenizer(strategy="simple", preserve_case=False)
        tokens2 = tokenizer2.tokenize(text)
        self.assertEqual(tokens2, ["hello", "world"])
    
    def test_punctuation_handling(self):
        """Test punctuation handling option."""
        text = "Hello, world!"
        # With punctuation (default)
        tokenizer1 = Tokenizer(strategy="simple", keep_punctuation=True)
        tokens1 = tokenizer1.tokenize(text)
        self.assertEqual(tokens1, ["Hello", ",", "world", "!"])
        
        # Without punctuation
        tokenizer2 = Tokenizer(strategy="simple", keep_punctuation=False)
        tokens2 = tokenizer2.tokenize(text)
        self.assertEqual(tokens2, ["Hello", "world"])
    
    def test_empty_text(self):
        """Test handling of empty text."""
        tokenizer = Tokenizer()
        self.assertEqual(tokenizer.tokenize(""), [])
        self.assertEqual(tokenizer.tokenize("   "), [])
    
    def test_type_error(self):
        """Test handling of non-string inputs."""
        tokenizer = Tokenizer()
        with self.assertRaises(TypeError):
            tokenizer.tokenize(123)
        with self.assertRaises(TypeError):
            tokenizer.tokenize(None)
    
    def test_tokens_with_metadata(self):
        """Test getting tokens with metadata."""
        text = "Hello, 123!"
        tokenizer = Tokenizer(strategy="simple")
        tokens_with_metadata = tokenizer.get_tokens_with_metadata(text)
        
        # Check structure and basic properties
        self.assertEqual(len(tokens_with_metadata), 4)  # "Hello", ",", "123", "!"
        
        # Check token properties
        self.assertEqual(tokens_with_metadata[0]["token"], "Hello")
        self.assertTrue(tokens_with_metadata[0]["is_alpha"])
        self.assertFalse(tokens_with_metadata[0]["is_digit"])
        self.assertFalse(tokens_with_metadata[0]["is_punct"])
        
        self.assertEqual(tokens_with_metadata[1]["token"], ",")
        self.assertFalse(tokens_with_metadata[1]["is_alpha"])
        self.assertFalse(tokens_with_metadata[1]["is_digit"])
        self.assertTrue(tokens_with_metadata[1]["is_punct"])
        
        self.assertEqual(tokens_with_metadata[2]["token"], "123")
        self.assertFalse(tokens_with_metadata[2]["is_alpha"])
        self.assertTrue(tokens_with_metadata[2]["is_digit"])
        self.assertFalse(tokens_with_metadata[2]["is_punct"])
    
    def test_invalid_strategy(self):
        """Test handling of invalid tokenization strategy."""
        with self.assertRaises(ValueError):
            Tokenizer(strategy="invalid_strategy")


class TestTokenizeText(unittest.TestCase):
    """Test cases for the tokenize_text function."""
    
    def test_function_interface(self):
        """Test the function interface with various options."""
        text = "Hello, WORLD!"
        
        # Default options
        tokens = tokenize_text(text)
        self.assertEqual(tokens, ["Hello", ",", "WORLD", "!"])
        
        # Custom options
        tokens = tokenize_text(
            text,
            strategy="simple",
            preserve_case=False,
            keep_punctuation=False
        )
        self.assertEqual(tokens, ["hello", "world"])


if __name__ == "__main__":
    unittest.main()
