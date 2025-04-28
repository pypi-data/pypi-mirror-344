"""
Error classes for AI Data SDK
"""

from typing import Dict, Optional, Any

class APIError(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
        
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - {self.details}"
        return self.message


class AuthenticationError(APIError):
    """Raised when authentication fails"""
    pass


class InvalidRequestError(APIError):
    """Raised when a request is invalid"""
    pass


class RateLimitError(APIError):
    """Raised when rate limits are exceeded"""
    pass
