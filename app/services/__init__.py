"""Service registry for shared instances."""

from app.services.cv_evaluation_service import CVEvaluationService

# Create singleton instances  
_cv_evaluation_service = None


def get_cv_evaluation_service() -> CVEvaluationService:
    """Get shared CV evaluation service instance."""
    global _cv_evaluation_service
    if _cv_evaluation_service is None:
        _cv_evaluation_service = CVEvaluationService()
    return _cv_evaluation_service