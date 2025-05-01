"""
Tests for the acace_text_preprocessor module.
"""

import unittest
from acace_text_preprocessor import TextPreprocessor, preprocess_text


class TestTextPreprocessor(unittest.TestCase):
    """Test cases for the TextPreprocessor class."""
    
    def test_html_removal(self):
        """Test removal of HTML tags and entities."""
        text = "<p>This is <b>bold</b> and this is an &amp; entity.</p>"
        preprocessor = TextPreprocessor(remove_html=True)
        result = preprocessor.preprocess(text)
        self.assertEqual(result, "This is bold and this is an & entity.")
    
    def test_unicode_normalization(self):
        """Test normalization of Unicode characters."""
        text = "café résumé"  # Contains combined forms
        preprocessor = TextPreprocessor(normalize_unicode=True)
        result = preprocessor.preprocess(text)
        self.assertEqual(result, "café résumé")  # Should be normalized
    
    def test_lowercase(self):
        """Test conversion to lowercase."""
        text = "This HAS Mixed CASE"
        preprocessor = TextPreprocessor(lowercase=True)
        result = preprocessor.preprocess(text)
        self.assertEqual(result, "this has mixed case")
    
    def test_whitespace_removal(self):
        """Test removal of redundant whitespace."""
        text = "  This   has \t  extra \n\n  whitespace.  "
        preprocessor = TextPreprocessor(remove_extra_whitespace=True)
        result = preprocessor.preprocess(text)
        self.assertEqual(result, "This has extra whitespace.")
    
    def test_all_options(self):
        """Test all preprocessing options together."""
        text = "  <div>This   HAS \t <b>HTML</b> &amp; extra \n\n  whitespace.  </div>"
        preprocessor = TextPreprocessor(
            remove_html=True,
            normalize_unicode=True,
            lowercase=True,
            remove_extra_whitespace=True
        )
        result = preprocessor.preprocess(text)
        self.assertEqual(result, "this has html & extra whitespace.")
    
    def test_empty_text(self):
        """Test handling of empty text."""
        preprocessor = TextPreprocessor()
        self.assertEqual(preprocessor.preprocess(""), "")
        self.assertEqual(preprocessor.preprocess("   "), "")
    
    def test_type_error(self):
        """Test handling of non-string inputs."""
        preprocessor = TextPreprocessor()
        with self.assertRaises(TypeError):
            preprocessor.preprocess(123)
        with self.assertRaises(TypeError):
            preprocessor.preprocess(None)


class TestPreprocessText(unittest.TestCase):
    """Test cases for the preprocess_text function."""
    
    def test_function_interface(self):
        """Test the function interface with various options."""
        text = "<p>This is <b>MIXED</b> case &amp; has   spaces.</p>"
        
        # Default options
        result = preprocess_text(text)
        self.assertEqual(result, "This is MIXED case & has spaces.")
        
        # Custom options
        result = preprocess_text(
            text,
            remove_html=True,
            normalize_unicode=True,
            lowercase=True,
            remove_extra_whitespace=True
        )
        self.assertEqual(result, "this is mixed case & has spaces.")


if __name__ == "__main__":
    unittest.main()
