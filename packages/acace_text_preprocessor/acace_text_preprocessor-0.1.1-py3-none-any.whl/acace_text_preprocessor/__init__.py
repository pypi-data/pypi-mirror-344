"""
ACACE Text Preprocessor Module

This module handles text preprocessing tasks like HTML cleaning and normalization.
"""

import re
import html

def preprocess_text(text: str) -> str:
    """
    Preprocess text by cleaning HTML and normalizing whitespace.
    
    Args:
        text: Input text to preprocess
        
    Returns:
        Cleaned and normalized text
    """
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

__all__ = ['preprocess_text']
