"""Custom exceptions for GitHub MCP Agent"""

class AgentError(Exception):
    """Base exception"""
    pass

class APIKeyMissingError(AgentError):
    """Missing API key"""
    pass
