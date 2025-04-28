"""
AI Data SDK - Python Client
A comprehensive SDK for standardizing, processing, embedding, and retrieving data for AI applications.
"""

__version__ = "0.1.1"  # Increment the version number

from .client import AIDataClient
from .errors import APIError, AuthenticationError, InvalidRequestError, RateLimitError

__all__ = [
    "AIDataClient",
    "APIError",
    "AuthenticationError", 
    "InvalidRequestError",
    "RateLimitError"
]
