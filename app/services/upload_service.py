"""Upload service for handling file operations."""

import logging
from typing import Dict, Optional
from uuid import UUID

from fastapi import UploadFile

from app.core.storage.file_manager import FileManager
from app.models.upload import Upload, UploadCreate, UploadStatus
from app.services.file_validator import FileValidator

logger = logging.getLogger(__name__)


class UploadService:
    """Service for handling file upload operations."""
    
    def __init__(self):
        """Initialize upload service with dependencies."""
        self.file_manager = FileManager()
        self.file_validator = FileValidator()
        self.uploads: Dict[UUID, Upload] = {}  # In-memory storage for now
    
    async def process_upload(self, file: UploadFile) -> tuple[bool, str, Optional[Upload]]:
        """
        Process an uploaded file.
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Tuple[bool, str, Optional[Upload]]: (success, message, upload_record)
        """
        logger.info(f"Processing upload: {file.filename}")
        
        # Validate file
        is_valid, error_message, file_type = self.file_validator.validate_file(file)
        if not is_valid:
            logger.warning(f"File validation failed: {error_message}")
            return False, error_message, None
        
        # Create upload record
        upload_data = UploadCreate(
            filename=file.filename,
            file_size=file.size,
            file_type=file_type
        )
        
        upload = Upload(
            filename=upload_data.filename,
            file_size=upload_data.file_size,
            file_type=upload_data.file_type,
            file_path="",  # Will be set after saving
            status=UploadStatus.PENDING
        )
        
        try:
            # Save file to storage
            file_path = self.file_manager.save_upload_file(
                upload.id, file.file, file.filename
            )
            upload.file_path = file_path
            
            # Store upload record
            self.uploads[upload.id] = upload
            
            logger.info(f"Upload successful: {upload.id}")
            return True, "File uploaded successfully", upload
            
        except Exception as e:
            error_msg = f"Failed to save file: {str(e)}"
            logger.error(error_msg)
            
            # Mark as failed if we created a record
            if upload.id in self.uploads:
                upload.status = UploadStatus.FAILED
                upload.error_message = error_msg
                self.uploads[upload.id] = upload
            
            return False, error_msg, None
    
    def get_upload(self, upload_id: UUID) -> Optional[Upload]:
        """
        Retrieve upload record by ID.
        
        Args:
            upload_id: Upload identifier
            
        Returns:
            Optional[Upload]: Upload record if found
        """
        return self.uploads.get(upload_id)
    
    def get_all_uploads(self) -> Dict[UUID, Upload]:
        """
        Get all upload records.
        
        Returns:
            Dict[UUID, Upload]: All upload records
        """
        return self.uploads.copy()
    
    def delete_upload(self, upload_id: UUID) -> bool:
        """
        Delete upload and associated file.
        
        Args:
            upload_id: Upload identifier
            
        Returns:
            bool: True if deleted successfully
        """
        upload = self.uploads.get(upload_id)
        if not upload:
            return False
        
        # Delete file from storage
        if upload.file_path:
            self.file_manager.delete_file(upload.file_path)
        
        # Remove from records
        del self.uploads[upload_id]
        
        logger.info(f"Upload deleted: {upload_id}")
        return True