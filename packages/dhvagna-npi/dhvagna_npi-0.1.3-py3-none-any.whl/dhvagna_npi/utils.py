"""
Utility functions for Dhvagna-NPI.

This module provides various utility functions used throughout the application.
"""

def get_language_name(lang_code):
    """Get readable language name from language code.
    
    Args:
        lang_code (str): Language code (e.g., 'en-US', 'hi-IN')
        
    Returns:
        str: Human-readable language name
    """
    language_names = {
        'en-US': 'English-US',
        'en-GB': 'English-GB',
        'es-ES': 'Spanish',
        'fr-FR': 'French',
        'de-DE': 'German',
        'zh-CN': 'Chinese',
        'hi-IN': 'Hindi',
        'te-IN': 'Telugu'
    }
    return language_names.get(lang_code, lang_code)

def get_available_languages():
    """Get dictionary of available languages with their codes.
    
    Returns:
        dict: Dictionary mapping option numbers to language descriptions
    """
    return {
        "1": "en-US (English - United States)",
        "2": "en-GB (English - United Kingdom)",
        "3": "es-ES (Spanish)",
        "4": "fr-FR (French)",
        "5": "de-DE (German)",
        "6": "zh-CN (Chinese - Mandarin)",
        "7": "hi-IN (Hindi)",
        "8": "te-IN (Telugu)"
    }

def get_language_codes():
    """Get mapping of option numbers to language codes.
    
    Returns:
        dict: Dictionary mapping option numbers to language codes
    """
    return {
        "1": "en-US", 
        "2": "en-GB", 
        "3": "es-ES", 
        "4": "fr-FR", 
        "5": "de-DE",
        "6": "zh-CN",
        "7": "hi-IN",
        "8": "te-IN"
    }