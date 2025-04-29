"""
Transcription history module for Dhvagna-NPI.

This module provides functionality to store, save, and retrieve transcription history.
"""

import os
import datetime

class TranscriptionHistory:
    """Class to manage the history of voice transcriptions."""
    
    def __init__(self, config):
        """Initialize the transcription history manager.
        
        Args:
            config: Configuration object containing settings for saving transcriptions.
        """
        self.config = config
        self.history = []
        
    def add(self, text):
        """Add transcription to history and save to file if enabled.
        
        Args:
            text (str): The transcribed text to add to history.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "text": text,
            "timestamp": timestamp
        })
        
        if self.config.save_transcriptions:
            filename = f"transcription_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(self.config.transcription_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Timestamp: {timestamp}\n\n{text}")
        
    def get_recent(self, count=5):
        """Get recent transcriptions.
        
        Args:
            count (int): Number of recent transcriptions to retrieve.
            
        Returns:
            list: List of recent transcription entries.
        """
        return self.history[-count:] if len(self.history) > 0 else []
        
    def get_saved_transcriptions(self, max_count=10):
        """Get saved transcription files from the configured folder.
        
        Args:
            max_count (int): Maximum number of transcription files to retrieve.
            
        Returns:
            list: List of tuples containing (filename, timestamp, content).
        """
        results = []
        
        if not self.config.save_transcriptions or not os.path.exists(self.config.transcription_folder):
            return results
            
        try:
            # Get all transcription files, sort by modified time (newest first)
            files = [(f, os.path.getmtime(os.path.join(self.config.transcription_folder, f))) 
                    for f in os.listdir(self.config.transcription_folder) 
                    if f.startswith("transcription_") and f.endswith(".txt")]
            
            files.sort(key=lambda x: x[1], reverse=True)  # Sort by modified time, newest first
            
            # Get the most recent files based on max_count
            for file_name, _ in files[:max_count]:
                file_path = os.path.join(self.config.transcription_folder, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract timestamp if it exists
                        timestamp = "Unknown"
                        if content.startswith("Timestamp:"):
                            timestamp_line = content.split('\n')[0]
                            timestamp = timestamp_line.replace("Timestamp:", "").strip()
                        
                        # Get the actual transcription text (after the timestamp lines)
                        text_content = '\n'.join(content.split('\n')[2:])
                        
                        results.append((file_name, timestamp, text_content))
                except Exception:
                    continue
        except Exception:
            pass
            
        return results