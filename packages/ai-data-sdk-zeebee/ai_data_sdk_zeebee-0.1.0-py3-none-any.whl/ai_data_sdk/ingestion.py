"""
Data Ingestion Module

This module provides utilities for ingesting and preprocessing data from various sources.
"""

import json
import logging
import re
import csv
from typing import List, Dict, Any, Union, Optional, Callable, TextIO, BinaryIO
from pathlib import Path

from .validation import InputValidationError

# Set up logging
logger = logging.getLogger(__name__)

class DataIngester:
    """
    Class for ingesting data from various sources and preprocessing it.
    """
    def __init__(self, preprocessors: Optional[List[Callable]] = None):
        """
        Initialize DataIngester.
        
        Args:
            preprocessors: Optional list of preprocessing functions to apply to text data
        """
        self.preprocessors = preprocessors or []
        self.logger = logger
        
    def load_from_json(self, source: Union[str, Path, TextIO, Dict], text_field: str = 'text') -> List[Dict]:
        """
        Load data from a JSON file or string.
        
        Args:
            source: JSON file path, JSON string, file-like object, or dictionary
            text_field: Field name containing the text to process
            
        Returns:
            List of document dictionaries
        """
        try:
            # Handle different source types
            if isinstance(source, dict):
                # Already a dictionary
                data = source
            elif isinstance(source, str):
                if source.lstrip().startswith('{') or source.lstrip().startswith('['):
                    # JSON string
                    data = json.loads(source)
                else:
                    # File path
                    with open(source, 'r', encoding='utf-8') as f:
                        data = json.load(f)
            elif hasattr(source, 'read'):
                # File-like object
                data = json.load(source)
            else:
                # Path object
                with open(source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
            # Handle different JSON structures
            documents = []
            if isinstance(data, list):
                # List of documents
                documents = data
            elif isinstance(data, dict):
                # Single document or dict with document list
                if text_field in data:
                    # Single document
                    documents = [data]
                elif any(isinstance(data.get(k), list) for k in data):
                    # Dictionary with document list
                    for key, value in data.items():
                        if isinstance(value, list):
                            documents.extend(value)
                else:
                    # Treat as single document
                    documents = [data]
                    
            # Validate documents
            valid_documents = []
            for doc in documents:
                if not isinstance(doc, dict):
                    self.logger.warning(f"Skipping non-dictionary document: {doc}")
                    continue
                    
                if text_field not in doc:
                    self.logger.warning(f"Document missing text field: {text_field}")
                    continue
                    
                if not isinstance(doc[text_field], str):
                    self.logger.warning(f"Document has non-string text field: {doc}")
                    continue
                    
                # Apply preprocessors
                doc[text_field] = self._preprocess_text(doc[text_field])
                valid_documents.append(doc)
                
            self.logger.info(f"Loaded {len(valid_documents)} documents from JSON source")
            return valid_documents
            
        except Exception as e:
            self.logger.error(f"Error loading from JSON: {str(e)}")
            raise InputValidationError(f"Failed to load data from JSON: {str(e)}")
            
    def load_from_csv(self, source: Union[str, Path, TextIO], text_field: Optional[str] = None, 
                    delimiter: str = ',', has_header: bool = True) -> List[Dict]:
        """
        Load data from a CSV file.
        
        Args:
            source: CSV file path or file-like object
            text_field: Column name or index for text data (if None, first column is used)
            delimiter: CSV delimiter character
            has_header: Whether the CSV file has a header row
            
        Returns:
            List of document dictionaries
        """
        try:
            # Open file if path is provided
            close_file = False
            if isinstance(source, (str, Path)):
                source = open(source, 'r', encoding='utf-8', newline='')
                close_file = True
                
            try:
                # Read CSV
                reader = csv.reader(source, delimiter=delimiter)
                
                # Process header
                headers = []
                if has_header:
                    headers = next(reader)
                    
                    # Determine text field index
                    text_field_index = 0
                    if text_field is not None:
                        if isinstance(text_field, str):
                            if text_field in headers:
                                text_field_index = headers.index(text_field)
                            else:
                                self.logger.warning(f"Text field '{text_field}' not found in headers, using first column")
                        elif isinstance(text_field, int) and 0 <= text_field < len(headers):
                            text_field_index = text_field
                        else:
                            self.logger.warning(f"Invalid text field index, using first column")
                else:
                    # Generate headers
                    text_field_index = 0 if text_field is None else (text_field if isinstance(text_field, int) else 0)
                    headers = [f"field_{i}" for i in range(1000)]  # Arbitrary large number
                    
                # Process rows
                documents = []
                for row in reader:
                    if not row:  # Skip empty rows
                        continue
                        
                    # Create document
                    doc = {}
                    for i, value in enumerate(row[:len(headers)]):
                        doc[headers[i]] = value
                        
                    # Make sure text field exists
                    if text_field_index < len(row):
                        text = row[text_field_index]
                        # Apply preprocessors
                        text = self._preprocess_text(text)
                        doc[headers[text_field_index]] = text
                        documents.append(doc)
                    else:
                        self.logger.warning(f"Row missing text field: {row}")
                        
                self.logger.info(f"Loaded {len(documents)} documents from CSV source")
                return documents
                
            finally:
                if close_file:
                    source.close()
                    
        except Exception as e:
            self.logger.error(f"Error loading from CSV: {str(e)}")
            raise InputValidationError(f"Failed to load data from CSV: {str(e)}")
            
    def load_from_text(self, source: Union[str, Path, TextIO], split_pattern: Optional[str] = None) -> List[Dict]:
        """
        Load data from a text file, optionally splitting into documents.
        
        Args:
            source: Text file path, string, or file-like object
            split_pattern: Optional regex pattern to split text into documents
            
        Returns:
            List of document dictionaries
        """
        try:
            # Load text content
            if isinstance(source, str):
                if '\n' in source or len(source) > 100:
                    # Treat as direct text content
                    text = source
                else:
                    # Treat as file path
                    with open(source, 'r', encoding='utf-8') as f:
                        text = f.read()
            elif hasattr(source, 'read'):
                # File-like object
                text = source.read()
            else:
                # Path object
                with open(source, 'r', encoding='utf-8') as f:
                    text = f.read()
                    
            # Split text into documents
            documents = []
            if split_pattern:
                # Split by pattern
                parts = re.split(split_pattern, text)
                for i, part in enumerate(parts):
                    if part.strip():  # Skip empty parts
                        # Apply preprocessors
                        processed_text = self._preprocess_text(part.strip())
                        documents.append({
                            'id': f'doc_{i}',
                            'text': processed_text
                        })
            else:
                # Treat as single document
                processed_text = self._preprocess_text(text)
                documents.append({
                    'id': 'doc_0',
                    'text': processed_text
                })
                
            self.logger.info(f"Loaded {len(documents)} documents from text source")
            return documents
            
        except Exception as e:
            self.logger.error(f"Error loading from text: {str(e)}")
            raise InputValidationError(f"Failed to load data from text: {str(e)}")
            
    def _preprocess_text(self, text: str) -> str:
        """Apply preprocessing functions to text."""
        processed = text
        for preprocessor in self.preprocessors:
            processed = preprocessor(processed)
        return processed
        
    def add_preprocessor(self, preprocessor: Callable[[str], str]) -> None:
        """Add a preprocessor function to the processing pipeline."""
        self.preprocessors.append(preprocessor)
        
# Common preprocessing functions
def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace from text."""
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Trim whitespace
    return text.strip()
    
def remove_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text)
    
def standardize_line_breaks(text: str) -> str:
    """Standardize line breaks in text."""
    # Convert various line break formats to \n
    text = re.sub(r'\r\n|\r', '\n', text)
    # Remove excessive line breaks
    return re.sub(r'\n{3,}', '\n\n', text)
    
# Convenience functions
def load_json_data(source: Union[str, Dict], text_field: str = 'text') -> List[Dict]:
    """Load data from JSON without instantiating a class."""
    ingester = DataIngester()
    return ingester.load_from_json(source, text_field)
    
def load_csv_data(source: Union[str, TextIO], text_field: Optional[str] = None, 
                delimiter: str = ',', has_header: bool = True) -> List[Dict]:
    """Load data from CSV without instantiating a class."""
    ingester = DataIngester()
    return ingester.load_from_csv(source, text_field, delimiter, has_header)
    
def load_text_data(source: Union[str, TextIO], split_pattern: Optional[str] = None) -> List[Dict]:
    """Load data from text without instantiating a class."""
    ingester = DataIngester()
    return ingester.load_from_text(source, split_pattern)