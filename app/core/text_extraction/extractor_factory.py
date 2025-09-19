"""Factory for creating appropriate text extractors."""

import logging
from typing import Dict, Optional

from app.core.text_extraction.base import TextExtractor
from app.core.text_extraction.docx_extractor import DocxExtractor
from app.core.text_extraction.pdf_extractor import PdfExtractor
from app.core.text_extraction.txt_extractor import TxtExtractor

logger = logging.getLogger(__name__)


class ExtractorFactory:
    """Factory for creating text extractors based on file type."""
    
    def __init__(self):
        """Initialize factory with available extractors."""
        self._extractors: Dict[str, TextExtractor] = {
            "txt": TxtExtractor(),
            "pdf": PdfExtractor(),
            "docx": DocxExtractor(),
        }
    
    def get_extractor(self, file_extension: str) -> Optional[TextExtractor]:
        """
        Get appropriate text extractor for file type.
        
        Args:
            file_extension: File extension (e.g., 'pdf', 'docx', 'txt')
            
        Returns:
            Optional[TextExtractor]: Extractor instance or None if not supported
        """
        extension = file_extension.lower().strip(".")
        
        extractor = self._extractors.get(extension)
        if extractor and extractor.supports_file_type(extension):
            logger.debug(f"Found extractor for file type: {extension}")
            return extractor
        
        logger.warning(f"No extractor available for file type: {extension}")
        return None
    
    def get_supported_types(self) -> list[str]:
        """
        Get list of supported file types.
        
        Returns:
            List[str]: List of supported file extensions
        """
        return list(self._extractors.keys())
    
    def is_supported(self, file_extension: str) -> bool:
        """
        Check if file type is supported.
        
        Args:
            file_extension: File extension to check
            
        Returns:
            bool: True if file type is supported
        """
        return self.get_extractor(file_extension) is not None