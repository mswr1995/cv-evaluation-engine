"""CV evaluation service combining text extraction and LLM analysis."""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

from app.core.text_extraction.extractor_factory import ExtractorFactory
from app.core.llm.llm_service import LLMService, CVEvaluationResult

logger = logging.getLogger(__name__)


class CVEvaluationService:
    """Service for complete CV evaluation pipeline."""
    
    def __init__(self, llm_model: str = "llama3.2:1b"):
        """Initialize CV evaluation service."""
        self.llm_service = LLMService(model_name=llm_model)
        self.extractor_factory = ExtractorFactory()
        logger.info("CVEvaluationService initialized")
    
    def setup_llm(self) -> bool:
        """Setup LLM model (download if needed)."""
        try:
            if not self.llm_service.pull_model_if_needed():
                logger.error("Failed to setup LLM model")
                return False
            logger.info("LLM model setup completed")
            return True
        except Exception as e:
            logger.error(f"Error setting up LLM: {e}")
            return False
    
    def evaluate_cv_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Complete CV evaluation pipeline: extract text + LLM analysis.
        
        Args:
            file_path: Path to CV file (PDF, DOCX, TXT)
            
        Returns:
            Dict containing evaluation results and metadata
        """
        try:
            # Step 1: Extract text from file
            logger.info(f"Extracting text from: {file_path}")
            logger.info(f"File path type: {type(file_path)}")
            logger.info(f"File path suffix: {file_path.suffix}")
            
            extractor = self.extractor_factory.get_extractor(file_path.suffix)
            if not extractor:
                return self._create_error_result(f"Unsupported file type: {file_path.suffix}")
            
            logger.info(f"Using extractor: {type(extractor).__name__}")
            
            # Call extract_text method
            result = extractor.extract_text(str(file_path))
            logger.info(f"Extractor result type: {type(result)}")
            logger.info(f"Extractor result: {result}")
            
            success, extracted_text, error_message = result
            
            if not success or not extracted_text.strip():
                error_msg = error_message if error_message else "No text could be extracted from CV"
                return self._create_error_result(error_msg)
            
            cv_text = extracted_text
            logger.info(f"Extracted {len(cv_text)} characters from CV")
            
            # Step 2: LLM evaluation
            logger.info("Starting LLM evaluation...")
            evaluation = self.llm_service.evaluate_cv(cv_text)
            
            # Step 3: Combine results
            result = {
                'success': True,
                'file_info': {
                    'filename': file_path.name,
                    'file_type': file_path.suffix.lower(),
                    'text_length': len(cv_text),
                    'extraction_metadata': {
                        'extractor_type': extractor.__class__.__name__,
                        'file_size': file_path.stat().st_size if file_path.exists() else 0
                    }
                },
                'evaluation': evaluation.model_dump(),
                'raw_text': cv_text[:1000] + "..." if len(cv_text) > 1000 else cv_text  # Truncate for response
            }
            
            logger.info(f"CV evaluation completed. Overall score: {evaluation.overall_score}/100")
            return result
            
        except Exception as e:
            logger.error(f"CV evaluation failed: {e}")
            return self._create_error_result(str(e))
    
    def evaluate_cv_text(self, cv_text: str, filename: str = "direct_input") -> Dict[str, Any]:
        """
        Evaluate CV from text input directly.
        
        Args:
            cv_text: Raw CV text content
            filename: Optional filename for metadata
            
        Returns:
            Dict containing evaluation results
        """
        try:
            if not cv_text or not cv_text.strip():
                return self._create_error_result("No text provided for evaluation")
            
            logger.info(f"Evaluating CV text ({len(cv_text)} characters)")
            
            # LLM evaluation
            evaluation = self.llm_service.evaluate_cv(cv_text)
            
            result = {
                'success': True,
                'file_info': {
                    'filename': filename,
                    'file_type': 'text',
                    'text_length': len(cv_text)
                },
                'evaluation': evaluation.model_dump(),
                'raw_text': cv_text[:1000] + "..." if len(cv_text) > 1000 else cv_text
            }
            
            logger.info(f"Text evaluation completed. Overall score: {evaluation.overall_score}/100")
            return result
            
        except Exception as e:
            logger.error(f"Text evaluation failed: {e}")
            return self._create_error_result(str(e))
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current LLM model status."""
        try:
            is_available = self.llm_service.is_model_available()
            return {
                'model_name': self.llm_service.model_name,
                'available': is_available,
                'status': 'ready' if is_available else 'not_available'
            }
        except Exception as e:
            logger.error(f"Error checking model status: {e}")
            return {
                'model_name': self.llm_service.model_name,
                'available': False,
                'status': 'error',
                'error': str(e)
            }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error result."""
        return {
            'success': False,
            'error': error_message,
            'evaluation': None,
            'file_info': None
        }