"""
Metadata Management Module

This module provides tools for managing and standardizing metadata for AI data.
"""

import logging
from typing import Dict, List, Any, Optional, Union

from .validation import InputValidationError

# Set up logging
logger = logging.getLogger(__name__)


class MetadataManager:
    """
    Class for managing metadata in AI data.
    """
    def __init__(self):
        """Initialize MetadataManager."""
        self.logger = logger
    
    def standardize_metadata(self, metadata: Dict) -> Dict:
        """
        Standardize metadata by ensuring all required fields are present.
        
        Args:
            metadata: Original metadata dictionary
            
        Returns:
            Standardized metadata dictionary
        """
        # Create a copy to avoid modifying the original
        result = metadata.copy()
        
        # Ensure required fields are present
        if 'id' not in result:
            # Generate a simple ID based on content hash if available
            if 'text' in result:
                result['id'] = f"doc_{hash(result['text'])}"
            else:
                result['id'] = f"doc_{hash(str(result))}"
        
        # Add timestamp if not present
        if 'timestamp' not in result:
            from datetime import datetime
            result['timestamp'] = datetime.utcnow().isoformat()
        
        return result
    
    def merge_metadata(self, metadata1: Dict, metadata2: Dict) -> Dict:
        """
        Merge two metadata dictionaries, giving priority to metadata1.
        
        Args:
            metadata1: Primary metadata dictionary
            metadata2: Secondary metadata dictionary (values used when not in metadata1)
            
        Returns:
            Merged metadata dictionary
        """
        # Start with metadata2 as base
        result = metadata2.copy()
        
        # Overwrite with metadata1 values
        result.update(metadata1)
        
        return result
    
    def extract_metadata(self, document: Dict, metadata_fields: List[str]) -> Dict:
        """
        Extract specified fields from a document as metadata.
        
        Args:
            document: Source document dictionary
            metadata_fields: List of field names to extract
            
        Returns:
            Extracted metadata dictionary
        """
        metadata = {}
        
        for field in metadata_fields:
            if field in document:
                metadata[field] = document[field]
        
        return metadata
    
    def add_metadata(self, documents: List[Dict], additional_metadata: Dict) -> List[Dict]:
        """
        Add additional metadata to a list of documents.
        
        Args:
            documents: List of document dictionaries
            additional_metadata: Metadata to add to each document
            
        Returns:
            Documents with added metadata
        """
        result = []
        
        for doc in documents:
            # Create a new document with the added metadata
            new_doc = doc.copy()
            
            # Add or update metadata
            for key, value in additional_metadata.items():
                new_doc[key] = value
            
            result.append(new_doc)
        
        return result


# Convenience functions
def standardize_document_metadata(document: Dict) -> Dict:
    """
    Standardize metadata for a single document without instantiating a class.
    
    Args:
        document: Document with metadata
        
    Returns:
        Document with standardized metadata
    """
    manager = MetadataManager()
    return manager.standardize_metadata(document)


def add_batch_metadata(documents: List[Dict], metadata: Dict) -> List[Dict]:
    """
    Add shared metadata to a batch of documents without instantiating a class.
    
    Args:
        documents: List of documents
        metadata: Shared metadata to add
        
    Returns:
        Documents with added metadata
    """
    manager = MetadataManager()
    return manager.add_metadata(documents, metadata)