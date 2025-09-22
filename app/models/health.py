"""Health check data models."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response for health check endpoint."""
    status: str
    message: str
    version: str = "1.0.0"
    environment: str = "development"