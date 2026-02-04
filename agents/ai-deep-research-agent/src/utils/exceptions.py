"""
Custom exceptions for AI Deep Research Agent
"""


class ResearchAgentError(Exception):
    """Base exception for research agent"""
    pass


class APIKeyMissingError(ResearchAgentError):
    """Raised when required API key is missing"""
    pass


class ResearchSourceError(ResearchAgentError):
    """Raised when research source fails"""
    pass


class RateLimitError(ResearchAgentError):
    """Raised when rate limit is exceeded"""
    pass


class InvalidInputError(ResearchAgentError):
    """Raised when input validation fails"""
    pass


class ModelError(ResearchAgentError):
    """Raised when LLM model fails"""
    pass
