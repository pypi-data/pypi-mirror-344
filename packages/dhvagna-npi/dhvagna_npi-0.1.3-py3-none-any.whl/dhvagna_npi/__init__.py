"""
Dhvagna-NPI - Advanced Voice Transcription Tool

A command-line tool for transcribing spoken audio to text in multiple languages.
"""

from .config import Config
from .history import TranscriptionHistory
from .core import main, run_single_transcription, run_interactive

__version__ = "0.1.3" 
__author__ = "dhvagna"