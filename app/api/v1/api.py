"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags = ["health"])