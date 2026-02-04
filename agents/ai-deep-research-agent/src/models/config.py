"""
AI Deep Research Agent Configuration Models
Type-safe configuration using Pydantic
"""
from typing import Literal, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class ModelConfig(BaseSettings):
    """LLM Model Configuration"""
    
    provider: Literal["openai", "anthropic", "google"] = Field(
        default="openai",
        description="LLM provider to use"
    )
    model_name: str = Field(
        default="gpt-4-turbo-preview",
        description="Specific model name"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Model temperature for response randomness"
    )
    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=128000,
        description="Maximum tokens in response"
    )
    
    class Config:
        env_prefix = "MODEL_"


class ResearchConfig(BaseSettings):
    """Research Agent Configuration"""
    
    max_papers: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of papers to retrieve"
    )
    max_depth: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum research depth (iterations)"
    )
    sources: list[str] = Field(
        default=["arxiv", "pubmed", "google_scholar"],
        description="Data sources to search"
    )
    enable_citations: bool = Field(
        default=True,
        description="Enable citation graph generation"
    )
    enable_knowledge_graph: bool = Field(
        default=True,
        description="Enable knowledge graph visualization"
    )
    
    class Config:
        env_prefix = "RESEARCH_"


class APIConfig(BaseSettings):
    """API Keys Configuration"""
    
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    google_api_key: Optional[str] = Field(default=None, description="Google API key")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class AppConfig(BaseSettings):
    """Application Configuration"""
    
    app_name: str = Field(
        default="AI Deep Research Agent",
        description="Application name"
    )
    version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )
    environment: Literal["development", "staging", "production"] = Field(
        default="production",
        description="Environment name"
    )
    max_requests_per_minute: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Rate limit for API requests"
    )
    
    class Config:
        env_prefix = "APP_"
