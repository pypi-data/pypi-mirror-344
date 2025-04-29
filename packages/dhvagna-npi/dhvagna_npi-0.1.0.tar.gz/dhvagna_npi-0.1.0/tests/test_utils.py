"""
Tests for the utils module.
"""

import unittest
from dhvagna_npi.config import Config
# Import the utility functions
from dhvagna_npi.utils import (
    get_language_name, 
    get_available_languages, 
    get_language_codes
)

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_get_language_name(self):
        """Test retrieving language names from codes."""
        # Test known languages
        self.assertEqual(get_language_name('en-US'), 'English-US')
        self.assertEqual(get_language_name('fr-FR'), 'French')
        self.assertEqual(get_language_name('zh-CN'), 'Chinese')
        self.assertEqual(get_language_name('te-IN'), 'Telugu')
        
        # Test unknown language (should return the code)
        self.assertEqual(get_language_name('xx-YY'), 'xx-YY')
        
        # Test empty string
        self.assertEqual(get_language_name(''), '')
        
        # Test None (should return None)
        self.assertEqual(get_language_name(None), None)

    def test_get_available_languages(self):
        """Test retrieving the available languages dictionary."""
        languages = get_available_languages()
        
        # Verify it's a dictionary
        self.assertIsInstance(languages, dict)
        
        # Verify it has the expected keys
        expected_keys = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for key in expected_keys:
            self.assertIn(key, languages)
        
        # Verify some values
        self.assertIn("English - United States", languages["1"])
        self.assertIn("Telugu", languages["8"])

    def test_get_language_codes(self):
        """Test retrieving the language codes dictionary."""
        codes = get_language_codes()
        
        # Verify it's a dictionary
        self.assertIsInstance(codes, dict)
        
        # Verify it has the expected keys
        expected_keys = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for key in expected_keys:
            self.assertIn(key, codes)
        
        # Verify values
        self.assertEqual(codes["1"], "en-US")
        self.assertEqual(codes["4"], "fr-FR")
        self.assertEqual(codes["8"], "te-IN")


if __name__ == '__main__':
    unittest.main()