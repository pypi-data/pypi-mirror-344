"""
Text preprocessing functionality for the ACACE pipeline.
"""

import re
import unicodedata
import html


class TextPreprocessor:
    """
    Class for cleaning and normalizing text inputs for further processing
    in the ACACE pipeline.
    """
    
    def __init__(self, remove_html=True, normalize_unicode=True, 
                 lowercase=False, remove_extra_whitespace=True):
        """
        Initialize the TextPreprocessor with configuration options.
        
        Args:
            remove_html (bool): Whether to remove HTML tags and decode HTML entities
            normalize_unicode (bool): Whether to normalize unicode characters
            lowercase (bool): Whether to convert text to lowercase
            remove_extra_whitespace (bool): Whether to remove redundant whitespace
        """
        self.remove_html = remove_html
        self.normalize_unicode = normalize_unicode
        self.lowercase = lowercase
        self.remove_extra_whitespace = remove_extra_whitespace
    
    def preprocess(self, text):
        """
        Preprocess the input text based on the configuration.
        
        Args:
            text (str): The text to preprocess
            
        Returns:
            str: The preprocessed text
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string")
        
        # Process empty text
        if not text.strip():
            return ""
        
        # Remove HTML tags and decode HTML entities
        if self.remove_html:
            text = re.sub(r'<[^>]+>', ' ', text)
            text = html.unescape(text)
        
        # Normalize unicode characters
        if self.normalize_unicode:
            text = unicodedata.normalize('NFKC', text)
        
        # Convert to lowercase if specified
        if self.lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        if self.remove_extra_whitespace:
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
        
        return text


def preprocess_text(text, **kwargs):
    """
    Utility function to preprocess text without explicitly creating a TextPreprocessor instance.
    
    Args:
        text (str): The text to preprocess
        **kwargs: Configuration options for TextPreprocessor
        
    Returns:
        str: The preprocessed text
    """
    preprocessor = TextPreprocessor(**kwargs)
    return preprocessor.preprocess(text)
