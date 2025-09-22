"""CV evaluation API endpoints."""

import logging
from pathlib import Path
from typing import Dict, Any

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from app.services.cv_evaluation_service import CVEvaluationService
from app.services.file_validator import FileValidator

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
cv_service = CVEvaluationService()
file_validator = FileValidator()


class TextEvaluationRequest(BaseModel):
    """Request model for text-based CV evaluation."""
    text: str
    filename: str = "direct_input.txt"


class EvaluationResponse(BaseModel):
    """Response model for CV evaluation results."""
    success: bool
    file_info: Dict[str, Any] = None
    evaluation: Dict[str, Any] = None
    error: str = None


@router.post("/evaluate-file", response_model=EvaluationResponse)
async def evaluate_cv_file(file: UploadFile = File(...)):
    """
    Evaluate CV from uploaded file using LLM analysis.
    
    Supports PDF, DOCX, and TXT files.
    Returns comprehensive evaluation with scores and insights.
    """
    try:
        # Validate file
        is_valid, error_message, file_type = file_validator.validate_file(file)
        if not is_valid:
            raise HTTPException(
                status_code=400, 
                detail=error_message
            )
        
        # Save uploaded file temporarily
        temp_path = Path(f"temp_uploads/{file.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Processing CV file: {file.filename}")
        
        # Evaluate CV
        result = cv_service.evaluate_cv_file(temp_path)
        
        # Cleanup
        try:
            temp_path.unlink()
        except:
            pass  # Ignore cleanup errors
        
        return EvaluationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CV evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate-text", response_model=EvaluationResponse)
async def evaluate_cv_text(request: TextEvaluationRequest):
    """
    Evaluate CV from raw text using LLM analysis.
    
    Accepts CV content as plain text and returns evaluation results.
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text content is required"
            )
        
        logger.info(f"Processing CV text ({len(request.text)} characters)")
        
        # Evaluate CV text
        result = cv_service.evaluate_cv_text(request.text, request.filename)
        
        return EvaluationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-status")
async def get_model_status():
    """
    Get current LLM model status and availability.
    
    Returns information about the Llama model setup.
    """
    try:
        status = cv_service.get_model_status()
        return status
    except Exception as e:
        logger.error(f"Model status error: {e}")
        return {
            'model_name': 'unknown',
            'available': False,
            'status': 'error',
            'error': str(e)
        }


@router.post("/setup-model")
async def setup_model():
    """
    Setup and download LLM model if needed.
    
    This endpoint may take several minutes on first run
    as it downloads the Llama model.
    """
    try:
        logger.info("Setting up LLM model...")
        success = cv_service.setup_llm()
        
        if success:
            return {
                'success': True,
                'message': 'LLM model setup completed successfully',
                'model_name': cv_service.llm_service.model_name
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to setup LLM model"
            )
            
    except Exception as e:
        logger.error(f"Model setup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported CV file formats."""
    return {
        'formats': ['pdf', 'docx', 'txt'],
        'max_file_size_mb': 10,
        'description': 'Upload CV files in PDF, DOCX, or TXT format for LLM-powered evaluation'
    }