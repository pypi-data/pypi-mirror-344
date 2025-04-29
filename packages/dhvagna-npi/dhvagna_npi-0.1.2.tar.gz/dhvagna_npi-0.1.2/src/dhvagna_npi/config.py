"""
Configuration module for Dhvagna-NPI.

This module provides functionality to store, load, and save user configuration settings.
"""

import os
import json
from pathlib import Path

class Config:
    """Configuration class to store settings for Dhvagna-NPI."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.hotkey = 'k'
        self.language = 'en-US'
        self.save_transcriptions = True
        # Use relative path for transcriptions folder
        self.transcription_folder = "transcriptions"
        self.theme = "default"
        self.timeout = 10
        self.energy_threshold = 300
        
        # Create transcription folder if it doesn't exist
        if not os.path.exists(self.transcription_folder):
            os.makedirs(self.transcription_folder)
            
    def save(self):
        """Save configuration to JSON file."""
        # Use relative path for config.json
        config_path = "config.json"
        with open(config_path, 'w') as f:
            json.dump({
                "hotkey": self.hotkey,
                "language": self.language,
                "save_transcriptions": self.save_transcriptions,
                "transcription_folder": self.transcription_folder,
                "theme": self.theme,
                "timeout": self.timeout,
                "energy_threshold": self.energy_threshold
            }, f, indent=4)
    
    @classmethod
    def load(cls):
        """Load configuration from JSON file.
        
        Returns:
            Config: A configuration object with values loaded from config.json or defaults.
        """
        config = cls()
        # Use relative path for config.json
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                try:
                    data = json.load(f)
                    config.hotkey = data.get("hotkey", 'k')
                    config.language = data.get("language", 'en-US')
                    config.save_transcriptions = data.get("save_transcriptions", True)
                    config.transcription_folder = data.get("transcription_folder", config.transcription_folder)
                    config.theme = data.get("theme", "default")
                    config.timeout = data.get("timeout", 10)
                    config.energy_threshold = data.get("energy_threshold", 300)
                except Exception:
                    # If there's an error, use default config
                    pass
        return config