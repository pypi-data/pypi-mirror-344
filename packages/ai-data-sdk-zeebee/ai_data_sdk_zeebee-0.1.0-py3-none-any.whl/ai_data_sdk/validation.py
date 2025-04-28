"""
Validation Module

This module provides tools for input validation and error handling.
"""

import logging
import json
from typing import Any, Dict, List, Optional, Union
import jsonschema

# Set up logging
logger = logging.getLogger(__name__)


# Custom exception classes
class AIDataSDKError(Exception):
    """Base exception class for AI Data SDK errors."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class InputValidationError(AIDataSDKError):
    """Exception raised for input validation errors."""
    pass


class APIError(AIDataSDKError):
    """Exception raised for API-related errors."""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict] = None):
        self.status_code = status_code
        super().__init__(message, details)


class DataQualityError(AIDataSDKError):
    """Exception raised for data quality issues."""
    pass


class EmbeddingError(AIDataSDKError):
    """Exception raised for embedding-related errors."""
    pass


class VectorDBError(AIDataSDKError):
    """Exception raised for vector database errors."""
    pass


class PIIError(AIDataSDKError):
    """Exception raised for PII detection errors."""
    pass


class FeedbackError(AIDataSDKError):
    """Exception raised for feedback-related errors."""
    pass


# JSON Schema Validation
def validate_schema(data: Any, schema: Dict) -> List[str]:
    """
    Validate data against a JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema to validate against
        
    Returns:
        List of validation errors, empty if valid
    """
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    
    if not errors:
        return []
        
    # Format error messages
    error_messages = []
    for error in errors:
        path = '.'.join(str(p) for p in error.path) if error.path else "<root>"
        message = f"{path}: {error.message}"
        error_messages.append(message)
        
    return error_messages


def validate_or_raise(data: Any, schema: Dict) -> None:
    """
    Validate data against a JSON schema and raise exception if invalid.
    
    Args:
        data: Data to validate
        schema: JSON schema to validate against
        
    Raises:
        InputValidationError: If validation fails
    """
    errors = validate_schema(data, schema)
    if errors:
        raise InputValidationError(
            f"Validation failed: {errors[0]}", 
            {"errors": errors}
        )


# Common validation schemas
EMBEDDING_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["texts"],
    "properties": {
        "texts": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "model": {"type": "string"}
    }
}

# Specialized validation functions
def validate_embedding_input(data: Any) -> None:
    """
    Validate input for embedding generation.
    
    Args:
        data: Input data to validate - either a list of strings or an object with 'texts' property
        
    Raises:
        InputValidationError: If validation fails
    """
    # If data is a list of strings, convert to expected object format
    if isinstance(data, list) and all(isinstance(item, str) for item in data):
        # Already a list of strings, wrap it in the expected format
        data = {"texts": data}
        
    validate_or_raise(data, EMBEDDING_REQUEST_SCHEMA)

SEARCH_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "embedding": {
            "type": "array",
            "items": {"type": "number"}
        },
        "top_k": {
            "type": "integer",
            "minimum": 1
        },
        "filters": {"type": "object"}
    },
    "oneOf": [
        {"required": ["query"]},
        {"required": ["embedding"]}
    ]
}

PII_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["text"],
    "properties": {
        "text": {"type": "string"},
        "mask": {"type": "boolean"},
        "pii_types": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

FEEDBACK_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["query_id", "result_id", "rating"],
    "properties": {
        "query_id": {"type": "string"},
        "result_id": {"type": "string"},
        "rating": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5
        },
        "comments": {"type": ["string", "null"]},
        "user_id": {"type": ["string", "null"]}
    }
}

TOKEN_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["user_id"],
    "properties": {
        "user_id": {"type": "string"},
        "expires_in": {
            "type": "integer",
            "minimum": 60,  # At least 1 minute
            "maximum": 86400  # Maximum 24 hours
        }
    }
}


# Helper functions
def format_error_response(error: AIDataSDKError) -> Dict:
    """Format an error for API response."""
    response = {
        "error": error.message,
        "details": error.details
    }
    
    if hasattr(error, "status_code"):
        response["status_code"] = error.status_code
        
    return response


def validate_type(value: Any, expected_type: type, param_name: str) -> None:
    """
    Validate that a value is of the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type
        param_name: Parameter name for error message
        
    Raises:
        InputValidationError: If type doesn't match
    """
    if not isinstance(value, expected_type):
        raise InputValidationError(
            f"Expected {param_name} to be of type {expected_type.__name__}, got {type(value).__name__}"
        )


def validate_dimensionality(vector: List[float], expected_dim: int) -> None:
    """
    Validate vector dimensionality.
    
    Args:
        vector: Vector to validate
        expected_dim: Expected dimension
        
    Raises:
        InputValidationError: If dimension doesn't match
    """
    if len(vector) != expected_dim:
        raise InputValidationError(
            f"Expected vector of dimension {expected_dim}, got {len(vector)}"
        )


def validate_text_nonempty(text: str, param_name: str) -> None:
    """
    Validate that a text string is not empty.
    
    Args:
        text: Text to validate
        param_name: Parameter name for error message
        
    Raises:
        InputValidationError: If text is empty
    """
    if not text.strip():
        raise InputValidationError(f"{param_name} cannot be empty")


def validate_batch_size(batch: List[Any], max_size: int) -> None:
    """
    Validate batch size.
    
    Args:
        batch: Batch to validate
        max_size: Maximum allowed size
        
    Raises:
        InputValidationError: If batch is too large
    """
    if len(batch) > max_size:
        raise InputValidationError(
            f"Batch size exceeds maximum allowed ({len(batch)} > {max_size})"
        )