"""Application configuration management."""

from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="CV Evaluation Engine")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # API
    api_v1_prefix: str = Field(default="/api/v1")
    docs_url: str = Field(default="/docs")
    redoc_url: str = Field(default="/redoc")
    
    # File Upload
    max_file_size_mb: int = Field(default=10)
    allowed_file_types: str = Field(default="pdf,txt,docx")
    
    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    
    @field_validator('allowed_file_types')
    def parse_file_types(cls, v: str) -> List[str]:
        """Convert comma-separated string to list of file types."""
        if isinstance(v, str):
            return [ft.strip().lower() for ft in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()