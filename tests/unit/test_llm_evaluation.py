"""Tests for LLM-powered CV evaluation."""

import pytest
from unittest.mock import Mock, patch
import json

from app.core.llm.llm_service import LLMService, CVEvaluationResult
from app.services.cv_evaluation_service import CVEvaluationService


class TestLLMService:
    """Test LLM service functionality."""
    
    @pytest.fixture
    def llm_service(self):
        """Create LLM service for testing."""
        return LLMService("test-model")
    
    def test_initialization(self, llm_service):
        """Test LLM service initialization."""
        assert llm_service.model_name == "test-model"
        assert llm_service.client is not None
    
    @patch('ollama.list')
    def test_is_model_available_success(self, mock_list, llm_service):
        """Test successful model availability check."""
        mock_list.return_value = {
            'models': [{'name': 'test-model'}, {'name': 'other-model'}]
        }
        
        assert llm_service.is_model_available() == True
    
    @patch('ollama.list')
    def test_is_model_available_not_found(self, mock_list, llm_service):
        """Test model not available."""
        mock_list.return_value = {
            'models': [{'name': 'other-model'}]
        }
        
        assert llm_service.is_model_available() == False
    
    @patch('ollama.list')
    def test_is_model_available_error(self, mock_list, llm_service):
        """Test error handling in model availability check."""
        mock_list.side_effect = Exception("Connection error")
        
        assert llm_service.is_model_available() == False
    
    def test_create_fallback_result(self, llm_service):
        """Test fallback result creation."""
        cv_text = "Python developer with SQL and pandas experience"
        result = llm_service._create_fallback_result(cv_text)
        
        assert isinstance(result, CVEvaluationResult)
        assert result.overall_score == 50
        assert result.skills_score > 0  # Should find some skills
        assert 'Python' in result.skills_found
    
    def test_extract_json_from_response_success(self, llm_service):
        """Test successful JSON extraction."""
        response_text = '''Here is the analysis:
        {
            "overall_score": 85,
            "skills_score": 40,
            "experience_score": 25,
            "education_score": 20,
            "skills_found": ["Python", "SQL"],
            "years_experience": 5,
            "education_level": "Master's",
            "detailed_analysis": "Strong candidate",
            "recommendations": ["Keep learning"],
            "market_insights": "Good position"
        }
        '''
        
        result = llm_service._extract_json_from_response(response_text)
        assert result['overall_score'] == 85
        assert result['skills_found'] == ["Python", "SQL"]
    
    def test_extract_json_from_response_invalid(self, llm_service):
        """Test JSON extraction failure."""
        response_text = "This is not valid JSON response"
        
        with pytest.raises(ValueError):
            llm_service._extract_json_from_response(response_text)
    
    @patch('ollama.chat')
    def test_evaluate_cv_success(self, mock_chat, llm_service):
        """Test successful CV evaluation."""
        mock_response = {
            'message': {
                'content': json.dumps({
                    "overall_score": 85,
                    "skills_score": 40,
                    "experience_score": 25,
                    "education_score": 20,
                    "skills_found": ["Python", "SQL", "Machine Learning"],
                    "years_experience": 5,
                    "education_level": "Master's Degree",
                    "detailed_analysis": "Strong data science candidate with relevant experience.",
                    "recommendations": ["Consider advanced ML certifications"],
                    "market_insights": "Well-positioned for senior roles"
                })
            }
        }
        mock_chat.return_value = mock_response
        
        cv_text = "Data scientist with 5 years experience in Python and ML"
        result = llm_service.evaluate_cv(cv_text)
        
        assert isinstance(result, CVEvaluationResult)
        assert result.overall_score == 85
        assert result.skills_score == 40
        assert "Python" in result.skills_found
        assert result.years_experience == 5
    
    @patch('ollama.chat')
    def test_evaluate_cv_llm_failure(self, mock_chat, llm_service):
        """Test CV evaluation with LLM failure."""
        mock_chat.side_effect = Exception("LLM service unavailable")
        
        cv_text = "Python developer"
        result = llm_service.evaluate_cv(cv_text)
        
        # Should return fallback result
        assert isinstance(result, CVEvaluationResult)
        assert result.overall_score == 50  # Fallback score


class TestCVEvaluationService:
    """Test CV evaluation service."""
    
    @pytest.fixture
    def cv_service(self):
        """Create CV evaluation service for testing."""
        with patch('app.services.cv_evaluation_service.LLMService'):
            return CVEvaluationService()
    
    def test_initialization(self, cv_service):
        """Test service initialization."""
        assert cv_service.llm_service is not None
        assert cv_service.extractor_factory is not None
    
    def test_evaluate_cv_text_empty(self, cv_service):
        """Test evaluation with empty text."""
        result = cv_service.evaluate_cv_text("")
        
        assert result['success'] == False
        assert 'No text provided' in result['error']
    
    def test_evaluate_cv_text_success(self, cv_service):
        """Test successful text evaluation."""
        # Mock the LLM service
        mock_evaluation = CVEvaluationResult(
            overall_score=80,
            skills_score=35,
            experience_score=25,
            education_score=20,
            skills_found=["Python", "SQL"],
            years_experience=4,
            education_level="Bachelor's",
            detailed_analysis="Good candidate",
            recommendations=["Learn more ML"],
            market_insights="Strong potential"
        )
        cv_service.llm_service.evaluate_cv.return_value = mock_evaluation
        
        cv_text = "Experienced Python developer with data science background"
        result = cv_service.evaluate_cv_text(cv_text)
        
        assert result['success'] == True
        assert result['evaluation']['overall_score'] == 80
        assert result['file_info']['text_length'] == len(cv_text)
    
    def test_get_model_status(self, cv_service):
        """Test model status retrieval."""
        cv_service.llm_service.is_model_available.return_value = True
        cv_service.llm_service.model_name = "test-model"
        
        status = cv_service.get_model_status()
        
        assert status['model_name'] == "test-model"
        assert status['available'] == True
        assert status['status'] == "ready"
    
    def test_create_error_result(self, cv_service):
        """Test error result creation."""
        error_msg = "Test error message"
        result = cv_service._create_error_result(error_msg)
        
        assert result['success'] == False
        assert result['error'] == error_msg
        assert result['evaluation'] is None