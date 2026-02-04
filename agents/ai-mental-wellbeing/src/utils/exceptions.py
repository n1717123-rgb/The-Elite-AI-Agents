"""Custom exceptions for AI Mental Wellbeing Coach"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
