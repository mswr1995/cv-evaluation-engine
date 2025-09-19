"""File validation utilities."""

import mimetypes
from pathlib import Path
from typing import Set, Tuple

from fastapi import UploadFile

from app.config import settings
from app.models.upload import FileType


class FileValidator:
    """Validates uploaded files for security and compatibility."""
    
    # MIME types for supported file formats
    ALLOWED_MIME_TYPES = {
        FileType.PDF: {"application/pdf"},
        FileType.TXT: {"text/plain", "text/csv"},
        FileType.DOCX: {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
    }
    
    def __init__(self):
        """Initialize validator with configured limits."""
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
        self.allowed_extensions = self._parse_allowed_extensions()
    
    def _parse_allowed_extensions(self) -> Set[str]:
        """Parse allowed file extensions from settings."""
        return {ext.lower().strip() for ext in settings.allowed_file_types}
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str, FileType]:
        """
        Validate uploaded file.
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Tuple[bool, str, FileType]: (is_valid, error_message, file_type)
        """
        # Check file size
        if file.size and file.size > self.max_file_size:
            max_size_mb = self.max_file_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_size_mb}MB", None
        
        # Check file extension
        file_extension = self._get_file_extension(file.filename)
        if file_extension not in self.allowed_extensions:
            allowed = ", ".join(self.allowed_extensions)
            return False, f"File type not supported. Allowed: {allowed}", None
        
        # Determine file type
        try:
            file_type = FileType(file_extension)
        except ValueError:
            return False, f"Unsupported file type: {file_extension}", None
        
        # Validate MIME type for security
        if not self._validate_mime_type(file, file_type):
            return False, "File content doesn't match extension", None
        
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
        return file.content_type in allowed_types
