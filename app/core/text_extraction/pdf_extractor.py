"""Text extractor for PDF files."""

import logging
from pathlib import Path
from typing import Tuple

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

from app.core.text_extraction.base import TextExtractor

logger = logging.getLogger(__name__)


class PdfExtractor(TextExtractor):
    """Text extractor for PDF files (.pdf)."""
    
    def __init__(self):
        """Initialize PDF extractor and check dependencies."""
        if PdfReader is None:
            logger.error("pypdf library not installed. PDF extraction will not work.")
    
    def extract_text(self, file_path: str) -> Tuple[bool, str, str]:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple[bool, str, str]: (success, extracted_text, error_message)
        """
        if PdfReader is None:
            error_msg = "pypdf library not installed"
            logger.error(error_msg)
            return False, "", error_msg
        
        logger.debug(f"Extracting text from PDF file: {file_path}")
        
        try:
            # Verify file exists
            if not Path(file_path).exists():
                error_msg = f"File not found: {file_path}"
                logger.error(error_msg)
                return False, "", error_msg
            
            # Read PDF file
            reader = PdfReader(file_path)
            
            # Check if PDF has pages
            if len(reader.pages) == 0:
                error_msg = "PDF file has no pages"
                logger.warning(error_msg)
                return False, "", error_msg
            
            # Extract text from all pages
            extracted_text = []
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():  # Only add non-empty pages
                        extracted_text.append(page_text)
                        logger.debug(f"Extracted {len(page_text)} characters from page {page_num}")
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {e}")
                    continue
            
            # Combine all page text
            full_text = "\n\n".join(extracted_text)
            
            if not full_text.strip():
                error_msg = "No readable text found in PDF"
                logger.warning(error_msg)
                return False, "", error_msg
            
            logger.debug(f"Successfully extracted {len(full_text)} total characters from PDF")
            return True, full_text, ""
            
        except Exception as e:
            error_msg = f"Failed to extract text from PDF: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def supports_file_type(self, file_extension: str) -> bool:
        """Check if this extractor supports PDF files."""
        return file_extension.lower() == "pdf"