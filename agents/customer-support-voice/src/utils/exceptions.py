"""Custom exceptions for Customer Support Voice Agent"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
