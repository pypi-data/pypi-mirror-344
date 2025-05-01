"""
Tokenization functionality for the ACACE pipeline.
"""

import re
from typing import List, Dict, Union, Optional, Any
import importlib.util


class Tokenizer:
    """
    Tokenizes preprocessed text into semantic units for the ACACE pipeline.
    
    This class provides multiple tokenization strategies:
    - Simple whitespace and punctuation-based tokenization
    - NLTK-based tokenization (if available)
    - spaCy-based tokenization (if available)
    """
    
    def __init__(self, 
                 strategy: str = "simple", 
                 preserve_case: bool = True,
                 keep_punctuation: bool = True,
                 language: str = "en",
                 **kwargs: Any):
        """
        Initialize the Tokenizer with configuration options.
        
        Args:
            strategy (str): Tokenization strategy to use ('simple', 'nltk', or 'spacy')
            preserve_case (bool): Whether to preserve the case of tokens
            keep_punctuation (bool): Whether to include punctuation as separate tokens
            language (str): Language code for language-specific tokenization (ISO 639-1)
            **kwargs: Additional options for specific tokenization strategies
        """
        self.strategy = strategy.lower()
        self.preserve_case = preserve_case
        self.keep_punctuation = keep_punctuation
        self.language = language
        self.options = kwargs
        
        # Validate and initialize chosen tokenization strategy
        self._validate_strategy()
        self._initialize_tokenizer()
    
    def _validate_strategy(self) -> None:
        """Validate the selected tokenization strategy."""
        valid_strategies = ["simple", "nltk", "spacy"]
        if self.strategy not in valid_strategies:
            raise ValueError(f"Invalid tokenization strategy: {self.strategy}. " 
                            f"Must be one of {valid_strategies}")
    
    def _initialize_tokenizer(self) -> None:
        """Initialize the appropriate tokenizer based on the selected strategy."""
        if self.strategy == "nltk":
            if not self._check_module_installed("nltk"):
                raise ImportError("NLTK is not installed. Please install it using: pip install nltk")
            
            # Import and prepare NLTK tokenizer
            import nltk
            try:
                nltk.data.find(f'tokenizers/punkt/{self.language}.pickle')
            except LookupError:
                nltk.download('punkt')
        
        elif self.strategy == "spacy":
            if not self._check_module_installed("spacy"):
                raise ImportError("spaCy is not installed. Please install it using: pip install spacy")
            
            # Import and prepare spaCy tokenizer
            import spacy
            try:
                # Load the appropriate language model
                language_code = self.language
                if language_code == "en":
                    model = "en_core_web_sm"
                else:
                    model = f"{language_code}_core_news_sm"
                
                # Check if the model is installed
                if not spacy.util.is_package(model):
                    raise ImportError(f"spaCy model '{model}' is not installed. "
                                    f"Please install it using: python -m spacy download {model}")
                
                self.nlp = spacy.load(model, disable=["parser", "ner"])
            except Exception as e:
                raise ImportError(f"Failed to load spaCy model: {str(e)}")
    
    @staticmethod
    def _check_module_installed(module_name: str) -> bool:
        """Check if a Python module is installed."""
        return importlib.util.find_spec(module_name) is not None
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text using the configured strategy.
        
        Args:
            text (str): The preprocessed text to tokenize
            
        Returns:
            List[str]: A list of tokens
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
        
        # Handle empty text
        if not text.strip():
            return []
        
        # Choose tokenization method based on strategy
        if self.strategy == "simple":
            tokens = self._simple_tokenize(text)
        elif self.strategy == "nltk":
            tokens = self._nltk_tokenize(text)
        elif self.strategy == "spacy":
            tokens = self._spacy_tokenize(text)
        else:
            tokens = self._simple_tokenize(text)  # Default to simple tokenization
        
        # Apply case preservation if needed
        if not self.preserve_case:
            tokens = [token.lower() for token in tokens]
        
        return tokens
    
    def _simple_tokenize(self, text: str) -> List[str]:
        """Simple whitespace and punctuation-based tokenization."""
        if self.keep_punctuation:
            # This pattern matches words, punctuation, or other symbols as separate tokens
            pattern = r'\b\w+\b|[^\w\s]'
            tokens = re.findall(pattern, text)
        else:
            # Split by whitespace and remove punctuation
            text = re.sub(r'[^\w\s]', '', text)
            tokens = text.split()
        
        return tokens
    
    def _nltk_tokenize(self, text: str) -> List[str]:
        """NLTK-based tokenization."""
        import nltk
        
        if self.keep_punctuation:
            tokens = nltk.word_tokenize(text, language=self.language)
        else:
            # Tokenize and then filter out punctuation
            all_tokens = nltk.word_tokenize(text, language=self.language)
            tokens = [token for token in all_tokens if token.isalnum()]
        
        return tokens
    
    def _spacy_tokenize(self, text: str) -> List[str]:
        """spaCy-based tokenization."""
        doc = self.nlp(text)
        
        if self.keep_punctuation:
            tokens = [token.text for token in doc]
        else:
            tokens = [token.text for token in doc if not token.is_punct]
        
        return tokens
    
    def get_tokens_with_metadata(self, text: str) -> List[Dict[str, Union[str, bool]]]:
        """
        Tokenize the text and include additional metadata for each token.
        
        Args:
            text (str): The preprocessed text to tokenize
            
        Returns:
            List[Dict]: A list of token dictionaries with metadata
                Each dictionary contains:
                - token (str): The token text
                - is_alpha (bool): Whether the token is alphabetic
                - is_digit (bool): Whether the token is a digit
                - is_punct (bool): Whether the token is punctuation
                - pos (str): Part of speech (only available with spaCy)
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
        
        # Handle empty text
        if not text.strip():
            return []
        
        # For spaCy, we can get rich metadata
        if self.strategy == "spacy":
            doc = self.nlp(text)
            tokens_with_metadata = [
                {
                    "token": token.text,
                    "is_alpha": token.is_alpha,
                    "is_digit": token.is_digit,
                    "is_punct": token.is_punct,
                    "pos": token.pos_,
                    "lemma": token.lemma_
                }
                for token in doc
            ]
        # For other strategies, we compute basic metadata
        else:
            tokens = self.tokenize(text)
            tokens_with_metadata = [
                {
                    "token": token,
                    "is_alpha": token.isalpha(),
                    "is_digit": token.isdigit(),
                    "is_punct": all(not c.isalnum() and not c.isspace() for c in token),
                    "pos": None,
                    "lemma": token.lower()
                }
                for token in tokens
            ]
        
        # Apply case preservation if needed
        if not self.preserve_case:
            for item in tokens_with_metadata:
                item["token"] = item["token"].lower()
        
        return tokens_with_metadata


def tokenize_text(text: str, **kwargs: Any) -> List[str]:
    """
    Utility function to tokenize text without explicitly creating a Tokenizer instance.
    
    Args:
        text (str): The preprocessed text to tokenize
        **kwargs: Configuration options for Tokenizer
        
    Returns:
        List[str]: A list of tokens
    """
    tokenizer = Tokenizer(**kwargs)
    return tokenizer.tokenize(text)
