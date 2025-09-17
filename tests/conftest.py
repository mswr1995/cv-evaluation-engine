"""Pytest configuration and fixture."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client for FastAPI application."""
    return TestClient(app)