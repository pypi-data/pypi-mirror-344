# ACACE Text Preprocessor

![PyPI](https://img.shields.io/pypi/v/acace_text_preprocessor)
![License](https://img.shields.io/github/license/Sumedh1599/acace)
![GitHub issues](https://img.shields.io/github/issues/Sumedh1599/acace)

## Overview

The **ACACE Text Preprocessor** is the first component in the Adaptive Context-Aware Content Engine (ACACE) pipeline. It cleans and normalizes text inputs to ensure consistency for downstream processing in AI content generation workflows.

This module provides a versatile text cleaning toolset that prepares raw text inputs before they're tokenized and semantically analyzed. By standardizing text formats and removing noise, it creates a foundation for accurate semantic compression and context-aware content generation.

## Features

- **HTML Removal**: Strips HTML tags and decodes HTML entities
- **Unicode Normalization**: Standardizes Unicode characters for consistent processing
- **Whitespace Handling**: Removes redundant spaces, tabs, and newlines
- **Configurability**: Flexible options to customize preprocessing behavior
- **Simple API**: Both class-based and functional interfaces for integration flexibility

## Installation

```bash
pip install acace_text_preprocessor
```

## Quick Start

```python
from acace_text_preprocessor import preprocess_text

# Using the simple function interface
clean_text = preprocess_text("This   has <b>extra</b> spaces &amp; HTML.")
print(clean_text)  # Output: "This has extra spaces & HTML."

# Using the class for more control
from acace_text_preprocessor import TextPreprocessor

preprocessor = TextPreprocessor(
    remove_html=True,
    normalize_unicode=True,
    lowercase=True,
    remove_extra_whitespace=True
)

clean_text = preprocessor.preprocess("This   has <b>extra</b> spaces &amp; HTML.")
print(clean_text)  # Output: "this has extra spaces & html."
```

## Configuration Options

The `TextPreprocessor` class accepts the following configuration options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `remove_html` | bool | `True` | Removes HTML tags and decodes HTML entities |
| `normalize_unicode` | bool | `True` | Normalizes Unicode characters (NFKC form) |
| `lowercase` | bool | `False` | Converts text to lowercase |
| `remove_extra_whitespace` | bool | `True` | Removes redundant whitespace |

## Integration with ACACE Pipeline

This module serves as the entry point for the ACACE pipeline, with its output feeding directly into the `acace_tokenizer` module. Example integration:

```python
from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text

# Process raw text through the pipeline
raw_text = "Your <i>raw</i> text with    spaces &amp; formatting."
clean_text = preprocess_text(raw_text)
tokens = tokenize_text(clean_text)
```

## Development

### Requirements

- Python 3.8+

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
