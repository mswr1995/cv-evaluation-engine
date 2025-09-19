"""Text cleaning and preprocessing utilities."""

import re
from typing import List


class TextCleaner:
    """Utilities for cleaning and preprocessing extracted text."""
    
    def __init__(self):
        """Initialize text cleaner with common patterns."""
        # Common patterns to clean
        self.whitespace_pattern = re.compile(r'\s+')
        self.special_chars_pattern = re.compile(r'[^\w\s\-@.(),]')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        # Updated phone pattern to handle common formats
        self.phone_pattern = re.compile(r'(?:\+?1[-.\s]?)?(?:\(?[0-9]{3}\)?[-.\s]?)?[0-9]{3}[-.\s]?[0-9]{4}')
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text for better processing.
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove excessive whitespace
        cleaned = self.whitespace_pattern.sub(' ', text)
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Text to normalize
            
        Returns:
            str: Text with normalized whitespace
        """
        if not text:
            return ""
        
        # Replace multiple whitespace with single space
        return self.whitespace_pattern.sub(' ', text).strip()
    
    def extract_contact_info(self, text: str) -> dict[str, List[str]]:
        """
        Extract contact information from text.
        
        Args:
            text: Text to extract contact info from
            
        Returns:
            Dict[str, List[str]]: Dictionary with emails and phone numbers
        """
        contact_info = {
            "emails": [],
            "phone_numbers": []
        }
        
        if not text:
            return contact_info
        
        # Extract emails
        emails = self.email_pattern.findall(text)
        contact_info["emails"] = list(set(emails))  # Remove duplicates
        
        # Extract phone numbers (updated pattern)
        phones = self.phone_pattern.findall(text)
        contact_info["phone_numbers"] = list(set(phones))  # Remove duplicates
        
        return contact_info
    
    def get_text_stats(self, text: str) -> dict[str, int]:
        """
        Get basic statistics about the text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dict[str, int]: Text statistics
        """
        if not text:
            return {
                "character_count": 0,
                "word_count": 0,
                "line_count": 0
            }
        
        return {
            "character_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(text.splitlines())
        }