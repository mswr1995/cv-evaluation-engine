"""File validation utilities."""

import logging
import mimetypes
from pathlib import Path
from typing import Set, Tuple

from fastapi import UploadFile

from app.config import settings
from app.models.file_types import FileType

logger = logging.getLogger(__name__)


class FileValidator:
    """Validates uploaded files for security and compatibility."""
    
    # MIME types for supported file formats
    ALLOWED_MIME_TYPES = {
        FileType.PDF: {"application/pdf"},
        FileType.TXT: {"text/plain", "text/csv"},
        FileType.DOCX: {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-word.document.macroEnabled.12",
            "application/octet-stream",  # Sometimes DOCX is sent as binary
            "application/zip"  # DOCX files are essentially ZIP archives
        }
    }
    
    def __init__(self):
        """Initialize validator with configured limits."""
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
        self.min_file_size = 1  # Minimum 1 byte
        self.allowed_extensions = self._parse_allowed_extensions()
    
    def _parse_allowed_extensions(self) -> Set[str]:
        """Parse allowed file extensions from settings."""
        extensions = {ext.lower().strip() for ext in settings.allowed_file_types}
        logger.info(f"Allowed file extensions: {extensions}")
        return extensions
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str, FileType]:
        """
        Validate uploaded file.
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Tuple[bool, str, FileType]: (is_valid, error_message, file_type)
        """
        # Check for empty file with better error message
        if file.size is not None and file.size < self.min_file_size:
            return False, "File is empty or too small. Please upload a file with content.", None
        
        # Check file size
        if file.size and file.size > self.max_file_size:
            max_size_mb = self.max_file_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_size_mb}MB", None
        
        # Check file extension
        file_extension = self._get_file_extension(file.filename)
        logger.info(f"File extension detected: '{file_extension}'")
        logger.info(f"Allowed extensions: {self.allowed_extensions}")
        
        if file_extension not in self.allowed_extensions:
            allowed = ", ".join(self.allowed_extensions)
            return False, f"File type not supported. Allowed: {allowed}", None
        
        # Determine file type by mapping extension to FileType
        extension_to_filetype = {
            "txt": FileType.TXT,
            "pdf": FileType.PDF,
            "docx": FileType.DOCX
        }
        
        file_type = extension_to_filetype.get(file_extension)
        if not file_type:
            return False, f"Unsupported file type: {file_extension}", None
        
        # Skip MIME type validation - file extension is sufficient
        # MIME types can vary by system and are unreliable
        return True, "", file_type
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename."""
        if not filename:
            return ""
        return Path(filename).suffix.lower().lstrip(".")
    
    def _validate_mime_type(self, file: UploadFile, file_type: FileType) -> bool:
        """
        Validate that file MIME type matches expected type.
        
        Args:
            file: UploadFile object
            file_type: Expected file type
            
        Returns:
            bool: True if MIME type is valid
        """
        if not file.content_type:
            return True  # Skip validation if no content type provided
        
        allowed_types = self.ALLOWED_MIME_TYPES.get(file_type, set())
        logger.info(f"File content_type: '{file.content_type}', file_type: {file_type}, allowed_types: {allowed_types}")
        is_valid = file.content_type in allowed_types
        logger.info(f"MIME type validation result: {is_valid}")
        return is_valid
