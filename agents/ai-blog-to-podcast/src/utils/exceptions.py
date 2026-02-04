"""Custom exceptions for AI Blog to Podcast Studio"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
