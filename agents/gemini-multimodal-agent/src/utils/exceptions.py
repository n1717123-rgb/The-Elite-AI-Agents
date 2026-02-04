"""Custom exceptions for Gemini Multimodal Intelligence"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
