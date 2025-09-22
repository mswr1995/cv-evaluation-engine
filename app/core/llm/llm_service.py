"""LLM service for CV evaluation using Ollama/Llama."""

import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

import ollama
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CVEvaluationResult(BaseModel):
    """Structured result from LLM CV evaluation."""
    overall_score: int  # 0-100
    skills_score: int   # 0-50
    experience_score: int  # 0-30
    education_score: int   # 0-20
    
    skills_found: list[str]
    years_experience: int
    education_level: str
    
    detailed_analysis: str
    recommendations: list[str]
    market_insights: str


class LLMService:
    """Service for interacting with Llama model via Ollama."""
    
    def __init__(self, model_name: str = "llama3.2:1b"):
        """Initialize LLM service with specified model."""
        self.model_name = model_name
        self.client = ollama
        logger.info(f"LLMService initialized with model: {model_name}")
    
    def is_model_available(self) -> bool:
        """Check if the Llama model is available."""
        try:
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            return self.model_name in available_models
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    def pull_model_if_needed(self) -> bool:
        """Pull the model if it's not available locally."""
        if self.is_model_available():
            logger.info(f"Model {self.model_name} is already available")
            return True
        
        try:
            logger.info(f"Pulling model {self.model_name}...")
            self.client.pull(self.model_name)
            logger.info(f"Successfully pulled model {self.model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {self.model_name}: {e}")
            return False
    
    def evaluate_cv(self, cv_text: str) -> CVEvaluationResult:
        """
        Evaluate CV using LLM and return structured results.
        
        Args:
            cv_text: Cleaned CV text content
            
        Returns:
            CVEvaluationResult: Structured evaluation results
        """
        prompt = self._create_cv_evaluation_prompt(cv_text)
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert CV evaluator specializing in data science roles. Always return valid JSON responses.'
                    },
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.1,  # Low temperature for consistent results
                    'top_p': 0.9,
                }
            )
            
            # Extract JSON from response
            response_text = response['message']['content']
            result_json = self._extract_json_from_response(response_text)
            
            return CVEvaluationResult(**result_json)
            
        except Exception as e:
            logger.error(f"LLM evaluation failed: {e}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # Return fallback result
            return self._create_fallback_result(cv_text)
    
    def _create_cv_evaluation_prompt(self, cv_text: str) -> str:
        """Create detailed prompt for CV evaluation."""
        return f"""
Analyze this CV for a data science professional and provide a comprehensive evaluation.

CV TEXT:
{cv_text}

EVALUATION REQUIREMENTS:
1. Overall Score (0-100): Holistic assessment of the candidate
2. Skills Score (0-50): Based on relevant data science skills found
3. Experience Score (0-30): Based on years and quality of experience
4. Education Score (0-20): Based on degree level and field relevance

SCORING GUIDELINES:
- Skills (50 points max): 
  * Python, R, SQL: 8-10 points each
  * ML libraries (pandas, sklearn, tensorflow): 6-8 points each
  * Statistics, Analytics tools: 4-6 points each
  * Visualization tools: 3-5 points each
  
- Experience (30 points max):
  * 0-1 years: 5-10 points
  * 2-3 years: 10-15 points  
  * 4-7 years: 15-25 points
  * 8+ years: 25-30 points
  
- Education (20 points max):
  * PhD in relevant field: 18-20 points
  * Master's in relevant field: 12-16 points
  * Bachelor's in relevant field: 8-12 points
  * Other degrees: 4-8 points

Return your analysis as JSON in this exact format (integers only for scores):
{{
    "overall_score": <integer 0-100>,
    "skills_score": <integer 0-50>,
    "experience_score": <integer 0-30>,
    "education_score": <integer 0-20>,
    "skills_found": ["skill1", "skill2", ...],
    "years_experience": <integer>,
    "education_level": "<highest degree>",
    "detailed_analysis": "<2-3 sentence analysis>",
    "recommendations": ["recommendation1", "recommendation2", ...],
    "market_insights": "<career advice and market positioning>"
}}

CRITICAL: Return ONLY integers for all scores. Do not return objects or breakdowns for scores.
"""
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response."""
        try:
            # Try to find JSON block in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                raw_json = json.loads(json_str)
                
                # Post-process to fix LLM format issues
                return self._normalize_llm_response(raw_json)
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON from response: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
    
    def _normalize_llm_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """Convert LLM response to expected format."""
        result = raw_json.copy()
        
        # Fix scores that might be objects instead of integers
        def extract_score(value, max_score):
            if isinstance(value, dict):
                # Sum up individual scores if it's a breakdown
                return min(sum(v for v in value.values() if isinstance(v, (int, float))), max_score)
            elif isinstance(value, (int, float)):
                return min(int(value), max_score)
            else:
                return 0
        
        result['skills_score'] = extract_score(result.get('skills_score', 0), 50)
        result['experience_score'] = extract_score(result.get('experience_score', 0), 30) 
        result['education_score'] = extract_score(result.get('education_score', 0), 20)
        result['overall_score'] = min(int(result.get('overall_score', 0)), 100)
        result['years_experience'] = int(result.get('years_experience', 0))
        
        return result
    
    def _create_fallback_result(self, cv_text: str) -> CVEvaluationResult:
        """Create fallback result if LLM fails."""
        # Simple fallback analysis
        skills_count = len([skill for skill in ['python', 'sql', 'pandas', 'machine learning'] 
                           if skill in cv_text.lower()])
        
        return CVEvaluationResult(
            overall_score=50,
            skills_score=min(25, skills_count * 5),
            experience_score=15,
            education_score=10,
            skills_found=['Python', 'SQL'] if skills_count > 0 else [],
            years_experience=2,
            education_level="Bachelor's",
            detailed_analysis="LLM analysis failed, showing basic fallback results.",
            recommendations=["Please try again or check LLM service"],
            market_insights="Unable to provide insights at this time"
        )