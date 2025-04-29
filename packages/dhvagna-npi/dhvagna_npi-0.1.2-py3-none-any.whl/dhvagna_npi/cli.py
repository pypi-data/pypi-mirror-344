"""
Command-line interface module for Dhvagna-NPI.

This module provides command-line argument parsing and entry points.
"""

import argparse
import sys

from .core import main, run_interactive, run_single_transcription

def parse_args():
    """Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Dhvagna-NPI - Advanced Voice Transcription Tool"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode (multiple transcriptions)"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information and exit"
    )
    
    return parser.parse_args()

def show_version():
    """Display version information."""
    from . import __version__
    print(f"Dhvagna-NPI version {__version__}")

def cli_main():
    """Main entry point for the command-line interface."""
    args = parse_args()
    
    if args.version:
        show_version()
        sys.exit(0)
        
    if args.interactive:
        run_interactive()
    else:
        run_single_transcription()

if __name__ == "__main__":
    cli_main()