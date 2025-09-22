"""Health check endpoints."""

from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", 
        message="CV evaluation engine is running",
        version="1.0.0",
        environment="development"
    )