"""Configuration models for AI Services Agency"""
from pydantic import Field
from pydantic_settings import BaseSettings


class APIConfig(BaseSettings):
    """API Keys Configuration"""
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    
    class Config:
        env_file = ".env"


class AppConfig(BaseSettings):
    """Application Configuration"""
    app_name: str = "AI Services Agency"
    version: str = "1.0.0"
    log_level: str = "INFO"
