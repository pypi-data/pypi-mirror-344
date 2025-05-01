"""
ACACE Text Preprocessor: Cleans and normalizes raw text inputs.

This module handles the preprocessing of text for the ACACE pipeline,
ensuring consistency for downstream processing.
"""

from .preprocessor import TextPreprocessor, preprocess_text

__all__ = ["TextPreprocessor", "preprocess_text"]
__version__ = "0.1.0"
