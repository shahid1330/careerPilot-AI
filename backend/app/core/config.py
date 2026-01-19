"""
Application Configuration
Loads environment variables and provides centralized configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application Settings
    APP_NAME: str = "CareerPilot AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Configuration (supports both individual vars and DATABASE_URL)
    DATABASE_URL: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # LLM Configuration (Phase 3)
    LLM_API_KEY: str
    LLM_MODEL_NAME: str = "llama-3.1-8b-instant"
    LLM_TIMEOUT: int = 30  # seconds
    LLM_MAX_TOKENS: int = 2048
    
    # CORS Settings (production-safe with environment variable support)
    CORS_ORIGINS: List[str] = []
    
    def get_cors_origins(self) -> List[str]:
        """
        Get CORS origins from environment or return defaults
        Supports comma-separated origins in CORS_ORIGINS env var
        """
        # Check if CORS_ORIGINS is already set as a list (from pydantic parsing)
        if isinstance(self.CORS_ORIGINS, list) and len(self.CORS_ORIGINS) > 0:
            return self.CORS_ORIGINS
        
        # Try to get from environment variable (comma-separated)
        env_origins = os.getenv("CORS_ORIGINS")
        if env_origins:
            # Split by comma and strip whitespace
            return [origin.strip() for origin in env_origins.split(",") if origin.strip()]
        
        # Fallback to localhost for development
        return ["http://localhost:3000"]
    
    @property
    def database_url(self) -> str:
        """
        Get the PostgreSQL database URL
        Supports both DATABASE_URL env var (production) and individual vars (local dev)
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Fallback to individual variables
        if all([self.DB_HOST, self.DB_PORT, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        raise ValueError("Database configuration missing. Set DATABASE_URL or individual DB_* variables")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
