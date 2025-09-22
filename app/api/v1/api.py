"""Main API router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, evaluation

api_router = APIRouter()

# Include endpoint routers with correct prefixes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])