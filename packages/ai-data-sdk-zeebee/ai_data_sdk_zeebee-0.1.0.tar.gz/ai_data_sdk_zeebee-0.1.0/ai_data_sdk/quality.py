"""
Data Quality Module

This module provides tools for validating data quality and enforcing data standards.
"""

import logging
from typing import List, Dict, Any, Union, Optional, Callable, TypeVar
import json
import jsonschema
from jsonschema.exceptions import ValidationError

from .validation import InputValidationError, DataQualityError

# Set up logging
logger = logging.getLogger(__name__)

# Type definitions
T = TypeVar('T')


class DataValidator:
    """
    Class for validating data quality and enforcing data standards.
    """
    def __init__(self, schema: Optional[Dict] = None, max_errors: int = 100):
        """
        Initialize DataValidator.
        
        Args:
            schema: Optional JSON schema for validation
            max_errors: Maximum number of errors to collect
        """
        self.schema = schema
        self.max_errors = max_errors
        self.logger = logger
        
    def validate_with_schema(self, data: Any) -> List[str]:
        """
        Validate data against JSON schema.
        
        Args:
            data: Data to validate
            
        Returns:
            List of validation error messages, empty if valid
        """
        if not self.schema:
            return ["No schema provided for validation"]
            
        validator = jsonschema.Draft7Validator(self.schema)
        errors = list(validator.iter_errors(data))
        
        if not errors:
            return []
            
        # Format error messages
        error_messages = []
        for error in errors[:self.max_errors]:
            path = '.'.join(str(p) for p in error.path) if error.path else "<root>"
            message = f"{path}: {error.message}"
            error_messages.append(message)
            
        if len(errors) > self.max_errors:
            error_messages.append(f"... and {len(errors) - self.max_errors} more errors")
            
        return error_messages
        
    def validate_with_function(self, data: Any, validation_fn: Callable[[Any], bool], 
                             error_message: str = "Data validation failed") -> List[str]:
        """
        Validate data using a custom validation function.
        
        Args:
            data: Data to validate
            validation_fn: Function that takes data and returns True if valid
            error_message: Error message if validation fails
            
        Returns:
            List of validation error messages, empty if valid
        """
        try:
            if validation_fn(data):
                return []
            else:
                return [error_message]
        except Exception as e:
            return [f"Validation function failed: {str(e)}"]
            
    def validate_structure(self, data: List[Dict], required_fields: List[str]) -> List[str]:
        """
        Validate the structure of a list of documents.
        
        Args:
            data: List of documents to validate
            required_fields: List of field names that must be present
            
        Returns:
            List of validation error messages, empty if valid
        """
        errors = []
        
        if not isinstance(data, list):
            return ["Data must be a list of documents"]
            
        for i, doc in enumerate(data):
            if not isinstance(doc, dict):
                errors.append(f"Document at index {i} must be a dictionary")
                continue
                
            for field in required_fields:
                if field not in doc:
                    errors.append(f"Document at index {i} missing required field: {field}")
                    
            if len(errors) >= self.max_errors:
                errors.append(f"... stopping after {self.max_errors} errors")
                break
                
        return errors
        
    def validate_text_length(self, data: List[Dict], text_field: str, 
                          min_length: int = 1, max_length: Optional[int] = None) -> List[str]:
        """
        Validate that text fields meet length requirements.
        
        Args:
            data: List of documents to validate
            text_field: Field name containing text to validate
            min_length: Minimum text length
            max_length: Optional maximum text length
            
        Returns:
            List of validation error messages, empty if valid
        """
        errors = []
        
        if not isinstance(data, list):
            return ["Data must be a list of documents"]
            
        for i, doc in enumerate(data):
            if not isinstance(doc, dict):
                errors.append(f"Document at index {i} must be a dictionary")
                continue
                
            if text_field not in doc:
                errors.append(f"Document at index {i} missing text field: {text_field}")
                continue
                
            text = doc[text_field]
            if not isinstance(text, str):
                errors.append(f"Document at index {i} has non-string {text_field}")
                continue
                
            if len(text) < min_length:
                errors.append(f"Document at index {i} has {text_field} shorter than minimum length ({len(text)} < {min_length})")
                
            if max_length is not None and len(text) > max_length:
                errors.append(f"Document at index {i} has {text_field} longer than maximum length ({len(text)} > {max_length})")
                
            if len(errors) >= self.max_errors:
                errors.append(f"... stopping after {self.max_errors} errors")
                break
                
        return errors
        
    def validate_and_filter(self, data: List[T], validator_fn: Callable[[T], bool]) -> List[T]:
        """
        Validate data and filter out invalid items.
        
        Args:
            data: List of items to validate
            validator_fn: Function that takes an item and returns True if valid
            
        Returns:
            List of valid items
        """
        valid_items = []
        invalid_count = 0
        
        for item in data:
            try:
                if validator_fn(item):
                    valid_items.append(item)
                else:
                    invalid_count += 1
            except Exception:
                invalid_count += 1
                
        if invalid_count > 0:
            self.logger.warning(f"Filtered out {invalid_count} invalid items")
            
        return valid_items
        
    def validate_and_raise(self, data: Any, schema: Optional[Dict] = None) -> None:
        """
        Validate data against schema and raise exception if invalid.
        
        Args:
            data: Data to validate
            schema: JSON schema (uses instance schema if None)
            
        Raises:
            DataQualityError: If validation fails
        """
        validation_schema = schema or self.schema
        if not validation_schema:
            raise ValueError("No schema provided for validation")
            
        try:
            jsonschema.validate(data, validation_schema)
        except ValidationError as e:
            path = '.'.join(str(p) for p in e.path) if e.path else "<root>"
            message = f"Validation error at {path}: {e.message}"
            self.logger.error(message)
            raise DataQualityError(message)


# Helper functions for schema creation
def create_text_document_schema(required_fields: Optional[List[str]] = None) -> Dict:
    """
    Create a JSON schema for text documents.
    
    Args:
        required_fields: List of required fields (defaults to ["id", "text"])
        
    Returns:
        JSON schema dictionary
    """
    req = required_fields or ["id", "text"]
    
    schema = {
        "type": "object",
        "required": req,
        "properties": {
            "id": {
                "type": "string",
                "description": "Unique identifier for the document"
            },
            "text": {
                "type": "string",
                "description": "Text content of the document"
            }
        },
        "additionalProperties": True
    }
    
    return schema


def create_embedding_schema(dimension: int = 1536) -> Dict:
    """
    Create a JSON schema for text embeddings.
    
    Args:
        dimension: Expected embedding dimension
        
    Returns:
        JSON schema dictionary
    """
    schema = {
        "type": "array",
        "items": {
            "type": "number"
        },
        "minItems": dimension,
        "maxItems": dimension
    }
    
    return schema


def create_document_with_embedding_schema(embedding_field: str = "_embedding", 
                                       embedding_dimension: int = 1536) -> Dict:
    """
    Create a JSON schema for documents with embeddings.
    
    Args:
        embedding_field: Field name containing embedding
        embedding_dimension: Expected embedding dimension
        
    Returns:
        JSON schema dictionary
    """
    text_schema = create_text_document_schema()
    embedding_schema = create_embedding_schema(embedding_dimension)
    
    schema = {
        "type": "object",
        "required": ["id", "text", embedding_field],
        "properties": {
            "id": text_schema["properties"]["id"],
            "text": text_schema["properties"]["text"],
            embedding_field: embedding_schema
        },
        "additionalProperties": True
    }
    
    return schema


# Convenience functions
def validate_documents(documents: List[Dict], required_fields: Optional[List[str]] = None) -> List[str]:
    """
    Validate documents without instantiating a class.
    
    Args:
        documents: List of documents to validate
        required_fields: List of required fields (defaults to ["id", "text"])
        
    Returns:
        List of validation error messages, empty if valid
    """
    validator = DataValidator()
    return validator.validate_structure(documents, required_fields or ["id", "text"])


def validate_json_data(data: Any, schema: Dict) -> List[str]:
    """
    Validate data against a JSON schema without instantiating a class.
    
    Args:
        data: Data to validate
        schema: JSON schema
        
    Returns:
        List of validation error messages, empty if valid
    """
    validator = DataValidator(schema=schema)
    return validator.validate_with_schema(data)


def filter_valid_documents(documents: List[Dict], required_fields: Optional[List[str]] = None) -> List[Dict]:
    """
    Filter out invalid documents without instantiating a class.
    
    Args:
        documents: List of documents to filter
        required_fields: List of required fields (defaults to ["id", "text"])
        
    Returns:
        List of valid documents
    """
    req = required_fields or ["id", "text"]
    
    def is_valid(doc):
        if not isinstance(doc, dict):
            return False
        return all(field in doc for field in req)
    
    validator = DataValidator()
    return validator.validate_and_filter(documents, is_valid)