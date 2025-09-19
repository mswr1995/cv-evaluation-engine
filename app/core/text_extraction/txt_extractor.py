"""Text extractor for plain text files."""

import logging
from typing import List, Tuple

from app.core.text_extraction.base import TextExtractor

logger = logging.getLogger(__name__)


class TxtExtractor(TextExtractor):
    """Text extractor for plain text files (.txt)."""
    
    # Common text file encodings to try
    SUPPORTED_ENCODINGS = ["utf-8", "utf-16", "iso-8859-1", "cp1252"]
    
    def extract_text(self, file_path: str) -> Tuple[bool, str, str]:
        """
        Extract text from a plain text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Tuple[bool, str, str]: (success, extracted_text, error_message)
        """
        logger.debug(f"Extracting text from TXT file: {file_path}")
        
        # Try different encodings
        for encoding in self.SUPPORTED_ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    content = file.read()
                    
                logger.debug(f"Successfully extracted {len(content)} characters using {encoding}")
                return True, content, ""
                
            except UnicodeDecodeError:
                logger.debug(f"Failed to decode with {encoding}, trying next encoding")
                continue
            except Exception as e:
                error_msg = f"Failed to read text file: {str(e)}"
                logger.error(error_msg)
                return False, "", error_msg
        
        # If all encodings failed
        error_msg = "Could not decode text file with any supported encoding"
        logger.error(error_msg)
        return False, "", error_msg
    
    def supports_file_type(self, file_extension: str) -> bool:
        """Check if this extractor supports TXT files."""
        return file_extension.lower() == "txt"