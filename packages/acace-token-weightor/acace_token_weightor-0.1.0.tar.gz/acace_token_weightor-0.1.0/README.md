# ACACE Token Weightor

![PyPI](https://img.shields.io/pypi/v/acace_token_weightor)
![License](https://img.shields.io/github/license/Sumedh1599/acace)
![GitHub issues](https://img.shields.io/github/issues/Sumedh1599/acace)

## Overview

The **ACACE Token Weightor** is the third component in the Adaptive Context-Aware Content Engine (ACACE) pipeline. It assigns semantic weights to tokens based on their importance, enabling intelligent filtering and prioritization during content compression.

This module provides multiple weighting strategies that can assign values to tokens based on their frequency, part of speech, custom criteria, or a hybrid approach. By quantifying token importance, it creates the foundation for semantic compression that preserves meaning while reducing token count.

## Features

- **Multiple Weighting Strategies**: 
  - TF-IDF-based weighting for importance based on frequency
  - Part-of-speech (POS) weighting for linguistic importance
  - Custom weighting for domain-specific priorities
  - Hybrid weighting that combines multiple strategies

- **Advanced NLP Integration**:
  - Optional spaCy integration for accurate POS tagging
  - NLTK support for enhanced stopwords recognition

- **Customizability**:
  - Configurable POS weight mappings
  - Custom weight overrides for specific tokens
  - Adjustable weighting parameters

- **Simple API**:
  - Both class-based and functional interfaces for flexibility

## Installation

### Basic Installation

```bash
pip install acace_token_weightor
```

### With Optional Dependencies

```bash
# Install with spaCy support
pip install "acace_token_weightor[spacy]"

# Install with NLTK support
pip install "acace_token_weightor[nltk]"

# Install with all optional dependencies
pip install "acace_token_weightor[all]"
```

If using spaCy, you'll also need to download language models:

```bash
# Download English model
python -m spacy download en_core_web_sm
```

## Quick Start

```python
from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text
from acace_token_weightor import assign_weights

# Preprocess, tokenize, and weight text
raw_text = "The Adaptive Context-Aware Content Engine optimizes token usage while ensuring content coherence."
clean_text = preprocess_text(raw_text)
tokens = tokenize_text(clean_text)

# Using the TF-IDF weighting strategy (default)
weighted_tokens = assign_weights(tokens)
for token_data in weighted_tokens:
    print(f"Token: {token_data['token']}, Weight: {token_data['weight']:.2f}")

# Using POS-based weighting with spaCy for more accuracy
weighted_tokens = assign_weights(tokens, strategy="pos", use_spacy=True)

# Using a hybrid approach (combining TF-IDF and POS weighting)
weighted_tokens = assign_weights(
    tokens, 
    strategy="hybrid", 
    use_spacy=True,
    tfidf_factor=0.7,  # Weight of TF-IDF in the hybrid calculation
    pos_factor=0.3     # Weight of POS in the hybrid calculation
)

# Using the class-based interface for more control
from acace_token_weightor import TokenWeightor

# Custom POS weights for tech content
custom_pos_weights = {
    'NOUN': 1.0,
    'PROPN': 1.0,
    'VERB': 0.7,
    'ADJ': 0.8,  # Higher weight for adjectives in technical content
    'ADV': 0.4,
    'NUM': 0.6,  # Higher weight for numbers in technical content
    'PRON': 0.2,
    'DET': 0.1,
    'ADP': 0.1,
    'CONJ': 0.1,
    'CCONJ': 0.1,
    'SCONJ': 0.1,
    'PUNCT': 0.0,
    'SYM': 0.3,  # Higher weight for symbols in technical content
    'X': 0.1,
}

# Custom weights for specific tokens
custom_token_weights = {
    "ACACE": 1.0,
    "Context-Aware": 0.9,
    "Content": 0.8,
    "Engine": 0.8,
}

weightor = TokenWeightor(
    strategy="hybrid",
    pos_weights=custom_pos_weights,
    custom_weights=custom_token_weights,
    use_spacy=True,
    language="en"
)

weighted_tokens = weightor.assign_weights(tokens, context=clean_text)
```

## Configuration Options

The `TokenWeightor` class accepts the following configuration options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strategy` | str | `"tfidf"` | Weighting strategy (`"tfidf"`, `"pos"`, `"custom"`, or `"hybrid"`) |
| `pos_weights` | Dict[str, float] | *(predefined)* | Weights for different parts of speech |
| `custom_weights` | Dict[str, float] | `{}` | Custom weights for specific tokens |
| `min_weight` | float | `0.0` | Minimum weight for normalization |
| `max_weight` | float | `1.0` | Maximum weight for normalization |
| `use_spacy` | bool | `False` | Whether to use spaCy for enhanced linguistic analysis |
| `language` | str | `"en"` | Language code for language-specific processing |

## Integration with ACACE Pipeline

This module is designed to work with previous ACACE components and feed into subsequent ones:

```python
from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text
from acace_token_weightor import assign_weights
from acace_token_filter import filter_tokens

# Process text through the pipeline
raw_text = "Your raw text here."
clean_text = preprocess_text(raw_text)
tokens = tokenize_text(clean_text)
weighted_tokens = assign_weights(tokens)
filtered_tokens = filter_tokens(weighted_tokens)
```

## Development

### Requirements

- Python 3.8+
- Optional dependencies: spaCy, NLTK

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
