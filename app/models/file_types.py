"""File-related data models for LLM evaluation system."""

from enum import Enum


class FileType(str, Enum):
    """Supported file types for CV evaluation."""
    TXT = "text/plain"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"