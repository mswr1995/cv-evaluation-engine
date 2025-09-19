"""Tests for text extraction functionality."""

import tempfile
from pathlib import Path

import pytest

from app.core.text_extraction.extractor_factory import ExtractorFactory
from app.core.text_extraction.text_cleaner import TextCleaner
from app.core.text_extraction.txt_extractor import TxtExtractor


class TestTxtExtractor:
    """Test cases for TXT text extractor."""
    
    def test_extract_simple_text(self):
        """Test extracting text from a simple text file."""
        extractor = TxtExtractor()
        
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            test_content = "This is a test CV.\nName: John Doe\nSkills: Python, FastAPI"
            f.write(test_content)
            temp_path = f.name
        
        try:
            success, text, error = extractor.extract_text(temp_path)
            
            assert success is True
            assert error == ""
            assert "John Doe" in text
            assert "Python" in text
        finally:
            Path(temp_path).unlink()  # Clean up
    
    def test_extract_nonexistent_file(self):
        """Test handling of non-existent files."""
        extractor = TxtExtractor()
        
        success, text, error = extractor.extract_text("nonexistent_file.txt")
        
        assert success is False
        assert text == ""
        assert "Failed to read text file" in error
    
    def test_supports_file_type(self):
        """Test file type support detection."""
        extractor = TxtExtractor()
        
        assert extractor.supports_file_type("txt") is True
        assert extractor.supports_file_type("TXT") is True
        assert extractor.supports_file_type("pdf") is False


class TestExtractorFactory:
    """Test cases for extractor factory."""
    
    def test_get_txt_extractor(self):
        """Test getting TXT extractor."""
        factory = ExtractorFactory()
        
        extractor = factory.get_extractor("txt")
        
        assert extractor is not None
        assert isinstance(extractor, TxtExtractor)
    
    def test_unsupported_file_type(self):
        """Test handling of unsupported file types."""
        factory = ExtractorFactory()
        
        extractor = factory.get_extractor("unsupported")
        
        assert extractor is None
    
    def test_get_supported_types(self):
        """Test getting list of supported file types."""
        factory = ExtractorFactory()
        
        supported = factory.get_supported_types()
        
        assert "txt" in supported
        assert "pdf" in supported
        assert "docx" in supported


class TestTextCleaner:
    """Test cases for text cleaner."""
    
    def test_clean_text(self):
        """Test basic text cleaning."""
        cleaner = TextCleaner()
        
        dirty_text = "  This   is    a   test  \n\n  with   extra   spaces  "
        cleaned = cleaner.clean_text(dirty_text)
        
        assert cleaned == "This is a test with extra spaces"
    
    def test_extract_contact_info(self):
        """Test contact information extraction."""
        cleaner = TextCleaner()
        
        text = "Contact me at john.doe@email.com or call 123-456-7890"
        contact_info = cleaner.extract_contact_info(text)
        
        assert "john.doe@email.com" in contact_info["emails"]
        assert len(contact_info["phone_numbers"]) > 0
    
    def test_get_text_stats(self):
        """Test text statistics calculation."""
        cleaner = TextCleaner()
        
        text = "Hello world\nThis is a test"
        stats = cleaner.get_text_stats(text)
        
        assert stats["character_count"] > 0
        assert stats["word_count"] == 6
        assert stats["line_count"] == 2