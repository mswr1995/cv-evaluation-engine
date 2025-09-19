"""File storage management utilities."""

import os
import shutil
from pathlib import Path
from typing import BinaryIO
from uuid import UUID

from app.config import settings


class FileManager:
    """Handles file storage operations."""
    
    def __init__(self):
        """Initialize file manager with storage paths."""
        self.upload_dir = Path("data/uploads")
        self.processed_dir = Path("data/processed")
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create storage directories if they don't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def save_upload_file(self, upload_id: UUID, file_content: BinaryIO, filename: str) -> str:
        """
        Save uploaded file to storage.
        
        Args:
            upload_id: Unique identifier for the upload
            file_content: Binary file content
            filename: Original filename
            
        Returns:
            str: Path where file was saved
            
        Raises:
            OSError: If file cannot be saved
        """
        # Create unique filename to avoid conflicts
        file_extension = Path(filename).suffix
        stored_filename = f"{upload_id}{file_extension}"
        file_path = self.upload_dir / stored_filename
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file_content, buffer)
            return str(file_path)
        except Exception as e:
            # Clean up partial file if save failed
            if file_path.exists():
                file_path.unlink()
            raise OSError(f"Failed to save file: {e}")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            bool: True if file was deleted, False if not found
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists in storage.
        
        Args:
            file_path: Path to check
            
        Returns:
            bool: True if file exists
        """
        return Path(file_path).exists()
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get size of stored file.
        
        Args:
            file_path: Path to file
            
        Returns:
            int: File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.stat().st_size