"""
Tests for the history module.
"""

import os
import unittest
import tempfile
from datetime import datetime

# Import the Config and TranscriptionHistory classes
from dhvagna_npi.config import Config
from dhvagna_npi.history import TranscriptionHistory

class TestTranscriptionHistory(unittest.TestCase):
    """Test cases for the TranscriptionHistory class."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        
        # Create a test config with the temporary directory
        self.config = Config()
        self.config.transcription_folder = os.path.join(self.test_dir.name, "transcriptions")
        if not os.path.exists(self.config.transcription_folder):
            os.makedirs(self.config.transcription_folder)
            
        # Create a history object
        self.history = TranscriptionHistory(self.config)

    def tearDown(self):
        """Clean up test environment."""
        self.test_dir.cleanup()

    def test_add_to_history(self):
        """Test adding transcriptions to history."""
        # Add some test transcriptions
        self.history.add("Test transcription 1")
        self.history.add("Test transcription 2")
        self.history.add("Test transcription 3")
        
        # Verify they're in the history
        self.assertEqual(len(self.history.history), 3)
        self.assertEqual(self.history.history[0]["text"], "Test transcription 1")
        self.assertEqual(self.history.history[1]["text"], "Test transcription 2")
        self.assertEqual(self.history.history[2]["text"], "Test transcription 3")
        
        # Verify timestamps exist
        for entry in self.history.history:
            self.assertIn("timestamp", entry)
            # Try to parse the timestamp to ensure it's valid
            datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")

    def test_get_recent(self):
        """Test retrieving recent transcriptions."""
        # Add some test transcriptions
        for i in range(10):
            self.history.add(f"Test transcription {i}")
            
        # Get the 5 most recent
        recent = self.history.get_recent(5)
        
        # Verify we got the right ones (most recent first)
        self.assertEqual(len(recent), 5)
        self.assertEqual(recent[0]["text"], "Test transcription 5")
        self.assertEqual(recent[4]["text"], "Test transcription 9")
        
        # Test with fewer items than requested
        few_history = TranscriptionHistory(self.config)
        few_history.add("Single entry")
        
        recent = few_history.get_recent(5)
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0]["text"], "Single entry")
        
        # Test with empty history
        empty_history = TranscriptionHistory(self.config)
        recent = empty_history.get_recent(5)
        self.assertEqual(len(recent), 0)

    def test_save_to_file(self):
        """Test saving transcriptions to files."""
        # Enable saving
        self.config.save_transcriptions = True
        
        # Add a transcription
        self.history.add("Test file transcription")
        
        # Check if a file was created
        files = os.listdir(self.config.transcription_folder)
        self.assertEqual(len(files), 1)
        
        # Verify the file contents
        filename = files[0]
        filepath = os.path.join(self.config.transcription_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test file transcription", content)
            self.assertIn("Timestamp:", content)

    def test_disable_saving(self):
        """Test disabling saving to files."""
        # Disable saving
        self.config.save_transcriptions = False
        
        # Add a transcription
        self.history.add("Unsaved transcription")
        
        # Check that no file was created
        files = os.listdir(self.config.transcription_folder)
        self.assertEqual(len(files), 0)


if __name__ == '__main__':
    unittest.main()