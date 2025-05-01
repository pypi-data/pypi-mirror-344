# ACACE Tokenizer

![PyPI](https://img.shields.io/pypi/v/acace_tokenizer)
![License](https://img.shields.io/github/license/Sumedh1599/acace)
![GitHub issues](https://img.shields.io/github/issues/Sumedh1599/acace)

## Overview

The **ACACE Tokenizer** is the second component in the Adaptive Context-Aware Content Engine (ACACE) pipeline. It converts preprocessed text into meaningful tokens that can be analyzed and weighted in subsequent processing steps.

This module provides multiple tokenization strategies, from simple whitespace-based splitting to advanced NLP-powered tokenization with spaCy or NLTK. The tokenizer creates the foundation for semantic analysis by breaking text into meaningful units while preserving important linguistic features.

## Features

- **Multiple Tokenization Strategies**: Choose from simple, NLTK, or spaCy-based tokenization
- **Metadata Enrichment**: Extract token-level metadata like part-of-speech and lemmas
- **Multilingual Support**: Process text in various languages (depending on strategy)
- **Configurability**: Control case preservation, punctuation handling, and other tokenization behaviors
- **Simple API**: Both class-based and functional interfaces for integration flexibility

## Installation

### Basic Installation

```bash
pip install acace_tokenizer
```

### With Optional Dependencies

```bash
# Install with NLTK support
pip install "acace_tokenizer[nltk]"

# Install with spaCy support
pip install "acace_tokenizer[spacy]"

# Install with all optional dependencies
pip install "acace_tokenizer[all]"
```

If using spaCy, you'll also need to download language models:

```bash
# Download English model
python -m spacy download en_core_web_sm

# Download other language models as needed
python -m spacy download fr_core_news_sm
```

## Quick Start

```python
from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text

# Preprocess and tokenize text
raw_text = "The quick brown fox jumped over the lazy dog."
clean_text = preprocess_text(raw_text)

# Using the simple tokenization strategy (default)
tokens = tokenize_text(clean_text)
print(tokens)  # Output: ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog', '.']

# Using NLTK for tokenization
tokens = tokenize_text(clean_text, strategy="nltk")
print(tokens)  # Output: ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog', '.']

# Using spaCy for tokenization
tokens = tokenize_text(clean_text, strategy="spacy")
print(tokens)  # Output: ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog', '.']

# Using the class-based interface for more control
from acace_tokenizer import Tokenizer

tokenizer = Tokenizer(
    strategy="spacy",
    preserve_case=False,
    keep_punctuation=False,
    language="en"
)

tokens = tokenizer.tokenize(clean_text)
print(tokens)  # Output: ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']

# Get tokens with metadata
tokens_with_metadata = tokenizer.get_tokens_with_metadata(clean_text)
for token_data in tokens_with_metadata:
    print(f"Token: {token_data['token']}, POS: {token_data['pos']}, Lemma: {token_data['lemma']}")
```

## Configuration Options

The `Tokenizer` class accepts the following configuration options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strategy` | str | `"simple"` | Tokenization strategy to use (`"simple"`, `"nltk"`, or `"spacy"`) |
| `preserve_case` | bool | `True` | Whether to preserve the case of tokens |
| `keep_punctuation` | bool | `True` | Whether to include punctuation as separate tokens |
| `language` | str | `"en"` | Language code for language-specific tokenization (ISO 639-1) |

## Integration with ACACE Pipeline

This module is designed to work seamlessly with other ACACE components:

```python
from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text
from acace_token_weightor import assign_weights

# Process text through the pipeline
raw_text = "Your raw text here."
clean_text = preprocess_text(raw_text)
tokens = tokenize_text(clean_text)
weighted_tokens = assign_weights(tokens)
```

## Development

### Requirements

- Python 3.8+
- Optional dependencies: NLTK, spaCy

### Testing

```bash
# Install development dependencies
pip install pytest

# Run tests
pytest
```

## License

MIT License

## Contributors

- Sumedh Patil ([@Sumedh1599](https://github.com/Sumedh1599))

## Acknowledgments

This module is part of the Adaptive Context-Aware Content Engine (ACACE), an open-source project designed to revolutionize AI-driven content writing by optimizing token usage and ensuring content coherence across multi-session tasks.
