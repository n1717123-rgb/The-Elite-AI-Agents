"""Custom exceptions for AI Sales Intelligence Team"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
