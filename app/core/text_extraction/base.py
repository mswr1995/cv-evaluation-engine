"""Base interface for text extractors."""

from abc import ABC, abstractmethod
from typing import Tuple


class TextExtractor(ABC):
    """Abstract base class for text extractors."""
    
    @abstractmethod
    def extract_text(self, file_path: str) -> Tuple[bool, str, str]:
        """
        Extract text from a file.
        
        Args:
            file_path: Path to the file to extract text from
            
        Returns:
            Tuple[bool, str, str]: (success, extracted_text, error_message)
            
        Note:
            If extraction fails, success=False and error_message contains details.
            If successful, success=True and extracted_text contains the content.
        """
        pass
    
    @abstractmethod
    def supports_file_type(self, file_extension: str) -> bool:
        """
        Check if this extractor supports the given file type.
        
        Args:
            file_extension: File extension (e.g., 'pdf', 'docx')
            
        Returns:
            bool: True if this extractor supports the file type
        """
        pass