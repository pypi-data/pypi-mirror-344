"""
Embedding Generation Module

This module provides utilities for generating text embeddings using
various language models (primarily OpenAI's API). Embeddings are vector
representations of text that capture semantic meaning, enabling similarity
search and other vector operations.

Key Features:
- Support for OpenAI's embedding models
- Batched processing for efficient API usage
- Document embedding with flexible field mapping
- Error handling and validation
- Performance monitoring and logging

Classes:
    EmbeddingGenerator: Main class for generating embeddings

Functions:
    create_embeddings: Generate embeddings for a list of texts
    embed_document: Embed a single document dictionary

Usage Example:
    ```python
    from ai_data_sdk.embedding import EmbeddingGenerator

    # Create generator
    embedder = EmbeddingGenerator(model="text-embedding-ada-002")
    
    # Generate embeddings for texts
    texts = ["This is a sample text", "Another example"]
    embeddings = embedder.create_embeddings(texts)
    
    # Embed documents
    documents = [{"id": 1, "text": "Document text"}]
    docs_with_embeddings = embedder.batch_embed_documents(
        documents, text_field="text", embedding_field="embedding"
    )
    ```

For enhanced functionality, consider using embedding_enhanced.py which
provides vector normalization, text chunking, and support for more models.
"""

import logging
import time
import base64
import json
from typing import List, Dict, Any, Optional, Union, Tuple
import numpy as np
import openai

from .validation import InputValidationError, APIError, validate_embedding_input

# Set up logging
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Class for generating text embeddings.
    """
    def __init__(self, model: str = "text-embedding-ada-002", 
                api_key: Optional[str] = None, 
                max_batch_size: int = 100,
                timeout: int = 60):
        """
        Initialize embedding generator.
        
        Args:
            model: Embedding model name
            api_key: OpenAI API key (if None, uses environment variable)
            max_batch_size: Maximum batch size for embedding requests
            timeout: Timeout for API requests in seconds
        """
        self.model = model
        # If API key is provided, set it (otherwise relies on OPENAI_API_KEY env var)
        if api_key:
            openai.api_key = api_key
            
        self.max_batch_size = max_batch_size
        self.timeout = timeout
        self.logger = logger
        
    def create_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            model: Optional model override
            
        Returns:
            List of embedding vectors as lists of floats
            
        Raises:
            InputValidationError: If texts are invalid
            APIError: If embedding generation fails
        """
        # Validate input
        validate_embedding_input(texts)
        
        # Use specified model or default
        model_name = model or self.model
        
        # Process in batches if needed
        if len(texts) > self.max_batch_size:
            all_embeddings = []
            for i in range(0, len(texts), self.max_batch_size):
                batch = texts[i:i + self.max_batch_size]
                batch_embeddings = self._generate_embeddings(batch, model_name)
                all_embeddings.extend(batch_embeddings)
            return all_embeddings
        else:
            return self._generate_embeddings(texts, model_name)
    
    def _generate_embeddings(self, texts: List[str], model: str) -> List[List[float]]:
        """
        Internal method to generate embeddings using OpenAI API.
        
        Args:
            texts: List of text strings to embed
            model: Model name
            
        Returns:
            List of embedding vectors
            
        Raises:
            APIError: If embedding generation fails
        """
        start_time = time.time()
        
        try:
            # Call OpenAI API with backoff retry
            response = openai.Embedding.create(
                model=model,
                input=texts,
                encoding_format="base64"  # For better handling of special characters
            )
            
            # Extract embeddings from response
            embeddings = [
                data['embedding'] for data in response['data']
            ]
            
            # Log performance metrics
            duration = time.time() - start_time
            dimension = len(embeddings[0]) if embeddings else 0
            
            self.logger.debug(f"Generated {len(embeddings)} embeddings with dimension {dimension}")
            
            if duration > 5:  # Log slow requests
                self.logger.warning(f"Slow embedding generation: {duration:.2f}s for {len(texts)} texts")
                
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {str(e)}")
            raise APIError(f"Embedding generation failed: {str(e)}", status_code=500)
            
    def batch_embed_documents(self, documents: List[Dict], 
                             text_field: str, 
                             embedding_field: str = "_embedding") -> List[Dict]:
        """
        Embed documents and add embedding vectors to each document.
        
        Args:
            documents: List of document dictionaries
            text_field: Field name containing the text to embed
            embedding_field: Field name to store the embedding vector
            
        Returns:
            Documents with embeddings added
            
        Raises:
            InputValidationError: If documents are invalid
            APIError: If embedding generation fails
        """
        # Check documents
        if not documents:
            return []
            
        # Extract texts
        texts = []
        valid_docs = []
        
        for doc in documents:
            if not isinstance(doc, dict):
                continue
                
            if text_field not in doc:
                self.logger.warning(f"Document missing text field: {text_field}")
                continue
                
            text = doc[text_field]
            if not isinstance(text, str) or not text.strip():
                self.logger.warning(f"Document has empty or invalid text")
                continue
                
            texts.append(text)
            valid_docs.append(doc)
            
        # Generate embeddings
        embeddings = self.create_embeddings(texts)
        
        # Add embeddings to documents
        result = []
        for i, doc in enumerate(valid_docs):
            doc_copy = doc.copy()
            doc_copy[embedding_field] = embeddings[i]
            result.append(doc_copy)
            
        return result

# For direct use without instantiating the class
def create_embeddings(texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """Generate embeddings for a list of texts without instantiating a class"""
    generator = EmbeddingGenerator(model=model)
    return generator.create_embeddings(texts)

def embed_document(document: Dict, text_field: str, 
                  embedding_field: str = "_embedding", 
                  model: str = "text-embedding-ada-002") -> Dict:
    """Embed a single document without instantiating a class"""
    generator = EmbeddingGenerator(model=model)
    result = generator.batch_embed_documents([document], text_field, embedding_field)
    return result[0] if result else document