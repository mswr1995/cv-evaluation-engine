"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Current application status and metadata
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment="development" if settings.debug else "production"
    )