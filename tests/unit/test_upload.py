"""Tests for file upload functionality."""

import io
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.models.upload import FileType


def test_upload_valid_text_file(client: TestClient) -> None:
    """Test uploading a valid text file."""
    # Create a test text file
    test_content = "This is a test CV content."
    test_file = io.BytesIO(test_content.encode())
    
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test_cv.txt", test_file, "text/plain")}
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert "upload_id" in data
    assert data["filename"] == "test_cv.txt"
    assert data["status"] == "pending"
    assert "message" in data


def test_upload_invalid_file_type(client: TestClient) -> None:
    """Test uploading an invalid file type."""
    test_content = b"fake image content"
    test_file = io.BytesIO(test_content)
    
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.jpg", test_file, "image/jpeg")}
    )
    
    assert response.status_code == 400
    assert "File type not supported" in response.json()["detail"]


def test_get_upload_by_id(client: TestClient) -> None:
    """Test retrieving upload by ID."""
    # First upload a file
    test_content = "Test CV content"
    test_file = io.BytesIO(test_content.encode())
    
    upload_response = client.post(
        "/api/v1/upload",
        files={"file": ("cv.txt", test_file, "text/plain")}
    )
    
    upload_id = upload_response.json()["upload_id"]
    
    # Then retrieve it
    get_response = client.get(f"/api/v1/upload/{upload_id}")
    
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == upload_id
    assert data["filename"] == "cv.txt"


def test_get_nonexistent_upload(client: TestClient) -> None:
    """Test retrieving non-existent upload."""
    fake_id = str(uuid4())
    
    response = client.get(f"/api/v1/upload/{fake_id}")
    
    assert response.status_code == 404
    assert "Upload not found" in response.json()["detail"]


def test_list_uploads(client: TestClient) -> None:
    """Test listing all uploads."""
    response = client.get("/api/v1/uploads")
    
    assert response.status_code == 200
    data = response.json()
    assert "uploads" in data
    assert "total_count" in data
    assert isinstance(data["uploads"], dict)