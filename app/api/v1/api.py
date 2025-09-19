"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, upload

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags = ["health"])
api_router.include_router(upload.router, tags = ["upload"])