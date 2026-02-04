"""Custom exceptions for AI Knowledge Base"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
