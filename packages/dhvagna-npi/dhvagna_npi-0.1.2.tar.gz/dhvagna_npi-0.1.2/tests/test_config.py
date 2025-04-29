"""
Tests for the config module.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

# Import the Config class from the package
from dhvagna_npi.config import Config

class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        # Save the original working directory
        self.original_dir = os.getcwd()
        # Change to the test directory
        os.chdir(self.test_dir.name)

    def tearDown(self):
        """Clean up test environment."""
        # Change back to the original directory
        os.chdir(self.original_dir)
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_default_config(self):
        """Test that default configuration values are set correctly."""
        config = Config()
        self.assertEqual(config.hotkey, 'k')
        self.assertEqual(config.language, 'en-US')
        self.assertTrue(config.save_transcriptions)
        self.assertEqual(config.transcription_folder, "transcriptions")
        self.assertEqual(config.theme, "default")
        self.assertEqual(config.timeout, 10)
        self.assertEqual(config.energy_threshold, 300)

    def test_save_load_config(self):
        """Test saving and loading configuration."""
        # Create a config with non-default values
        config = Config()
        config.hotkey = 'x'
        config.language = 'fr-FR'
        config.save_transcriptions = False
        config.transcription_folder = "custom_folder"
        config.theme = "dark"
        config.timeout = 15
        config.energy_threshold = 500
        
        # Save the config
        config.save()
        
        # Verify the config file exists
        self.assertTrue(os.path.exists("config.json"))
        
        # Load the config in a new instance
        loaded_config = Config.load()
        
        # Verify the loaded values match the saved values
        self.assertEqual(loaded_config.hotkey, 'x')
        self.assertEqual(loaded_config.language, 'fr-FR')
        self.assertFalse(loaded_config.save_transcriptions)
        self.assertEqual(loaded_config.transcription_folder, "custom_folder")
        self.assertEqual(loaded_config.theme, "dark")
        self.assertEqual(loaded_config.timeout, 15)
        self.assertEqual(loaded_config.energy_threshold, 500)

    def test_transcription_folder_creation(self):
        """Test that the transcription folder is created if it doesn't exist."""
        # Create a new config with a custom folder
        config = Config()
        config.transcription_folder = "test_transcriptions"
        
        # Check that the folder was created
        self.assertTrue(os.path.exists("test_transcriptions"))
        self.assertTrue(os.path.isdir("test_transcriptions"))

    def test_load_invalid_config(self):
        """Test loading with an invalid config file."""
        # Create an invalid JSON file
        with open("config.json", 'w') as f:
            f.write("This is not valid JSON")
        
        # Load the config, should use defaults
        config = Config.load()
        
        # Verify default values are used
        self.assertEqual(config.hotkey, 'k')
        self.assertEqual(config.language, 'en-US')
        self.assertTrue(config.save_transcriptions)


if __name__ == '__main__':
    unittest.main()