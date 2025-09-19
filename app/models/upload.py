"""Upload-related data models."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UploadStatus(str, Enum):
    """Upload processing status."""
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"


class FileType(str, Enum):
    """Supported file types."""
    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"


class UploadCreate(BaseModel):
    """Data for creating a new upload."""
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., ge=1, description="File size in bytes")
    file_type: FileType = Field(..., description="File type")


class Upload(BaseModel):
    """Upload record with full metadata."""
    id: UUID = Field(default_factory=uuid4, description="Unique upload identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    file_type: FileType = Field(..., description="File type")
    file_path: str = Field(..., description="Stored file path")
    status: UploadStatus = Field(default=UploadStatus.PENDING, description="Processing status")
    created_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class UploadResponse(BaseModel):
    """Response for successful upload."""
    upload_id: UUID = Field(..., description="Unique upload identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    status: UploadStatus = Field(..., description="Current status")
    message: str = Field(..., description="Response message")


class UploadListResponse(BaseModel):
    """Response for listing uploads."""
    uploads: dict[UUID, Upload]
    total_count: int