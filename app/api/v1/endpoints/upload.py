"""File upload endpoints."""

import logging
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.upload import Upload, UploadListResponse, UploadResponse
from app.services.upload_service import UploadService

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instance
upload_service = UploadService()


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload a CV file for processing.
    
    Args:
        file: CV file (PDF, TXT, or DOCX)
        
    Returns:
        UploadResponse: Upload confirmation with ID
        
    Raises:
        HTTPException: If upload fails
    """
    logger.info(f"Upload request received: {file.filename}")
    
    success, message, upload = await upload_service.process_upload(file)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return UploadResponse(
        upload_id=upload.id,
        filename=upload.filename,
        file_size=upload.file_size,
        status=upload.status,
        message=message
    )


@router.get("/upload/{upload_id}", response_model=Upload)
async def get_upload(upload_id: UUID) -> Upload:
    """
    Get upload details by ID.
    
    Args:
        upload_id: Upload identifier
        
    Returns:
        Upload: Upload record with metadata
        
    Raises:
        HTTPException: If upload not found
    """
    upload = upload_service.get_upload(upload_id)
    
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )
    
    return upload


@router.get("/uploads", response_model=UploadListResponse)
async def list_uploads() -> UploadListResponse:
    """
    List all uploads.
    
    Returns:
        UploadListResponse: All upload records
    """
    uploads = upload_service.get_all_uploads()
    
    return UploadListResponse(
        uploads=uploads,
        total_count=len(uploads)
    )


@router.delete("/upload/{upload_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_upload(upload_id: UUID) -> None:
    """
    Delete upload and associated file.
    
    Args:
        upload_id: Upload identifier
        
    Raises:
        HTTPException: If upload not found
    """
    success = upload_service.delete_upload(upload_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found"
        )