"""
Enhanced Embedding Generation Module

This module provides advanced utilities for generating text embeddings using
various language models including OpenAI's latest models with support
for other embedding providers, vector normalization, and text chunking.

Key Features:
- Support for latest OpenAI embedding models (text-embedding-3-small/large)
- Vector normalization for improved similarity search
- Text chunking with overlapping segments for large documents
- Multiple provider support with a unified interface
- Extensible architecture for adding new embedding providers
- Automatic dimension detection based on model
- Configurable batch processing for optimal performance

Classes:
    EnhancedEmbeddingGenerator: Advanced class for generating embeddings

Functions:
    create_embeddings: Generate embeddings for a list of texts
    embed_document: Embed a single document dictionary
    embed_and_chunk_text: Split text into chunks and embed each chunk

Usage Example:
    ```python
    from ai_data_sdk.embedding_enhanced import EnhancedEmbeddingGenerator
    
    # Create generator with vector normalization
    embedder = EnhancedEmbeddingGenerator(
        model="text-embedding-3-small",
        normalize_vectors=True
    )
    
    # Generate embeddings
    texts = ["This is a sample text", "Another example"]
    embeddings = embedder.create_embeddings(texts)
    
    # Chunk and embed a long document
    chunks = embedder.embed_chunks(
        long_text,
        chunk_size=512,
        chunk_overlap=128
    )
    ```

This module extends the base embedding.py module with more advanced features
and is recommended for most production use cases.
"""

import logging
import time
import base64
import json
import os
from typing import List, Dict, Any, Optional, Union, Tuple, Callable
import numpy as np

# Import OpenAI for API access
import openai

# Import validation modules
from .validation import InputValidationError, APIError, validate_embedding_input

# Set up logging
logger = logging.getLogger(__name__)

class EnhancedEmbeddingGenerator:
    """
    Enhanced class for generating text embeddings with multiple model support.
    """
    # Supported OpenAI models and their dimensions
    MODEL_DIMENSIONS = {
        # Older models
        "text-embedding-ada-002": 1536,
        # Newer models (post April 2024)
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        # Add other models as they become available
    }
    
    def __init__(self, 
                model: str = "text-embedding-3-small", 
                api_key: Optional[str] = None, 
                max_batch_size: int = 100,
                timeout: int = 60,
                provider: str = "openai",
                dimensions: Optional[int] = None,
                normalize_vectors: bool = True):
        """
        Initialize enhanced embedding generator.
        
        Args:
            model: Embedding model name
            api_key: API key (if None, uses environment variable)
            max_batch_size: Maximum batch size for embedding requests
            timeout: Timeout for API requests in seconds
            provider: Embedding provider (openai, other)
            dimensions: Override dimension for custom models
            normalize_vectors: Whether to normalize vectors (recommended for cosine similarity)
        """
        self.model = model
        self.provider = provider.lower()
        
        # Set up provider-specific configurations
        if self.provider == "openai":
            # If API key is provided, set it (otherwise relies on OPENAI_API_KEY env var)
            if api_key:
                openai.api_key = api_key
                
            # Validate OpenAI model
            if model not in self.MODEL_DIMENSIONS and not dimensions:
                logger.warning(f"Unknown OpenAI model: {model}. Defaulting to text-embedding-3-small.")
                self.model = "text-embedding-3-small"
                
            # Determine embedding dimensions
            self.dimensions = dimensions or self.MODEL_DIMENSIONS.get(model, 1536)
        else:
            # For custom providers, dimensions must be specified
            if not dimensions:
                raise ValueError(f"Dimensions must be specified for provider: {provider}")
            self.dimensions = dimensions
            
        self.max_batch_size = max_batch_size
        self.timeout = timeout
        self.normalize_vectors = normalize_vectors
        self.logger = logger
        
        logger.info(f"Initialized EnhancedEmbeddingGenerator with {model} model ({provider} provider)")
        
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
        Internal method to generate embeddings using the appropriate provider.
        
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
            # Use appropriate provider
            if self.provider == "openai":
                embeddings = self._generate_openai_embeddings(texts, model)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
            # Normalize vectors if requested
            if self.normalize_vectors:
                embeddings = [self._normalize_vector(emb) for emb in embeddings]
                
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
            
    def _generate_openai_embeddings(self, texts: List[str], model: str) -> List[List[float]]:
        """Generate embeddings using OpenAI API."""
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        
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
        
        return embeddings
        
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize vector to unit length for cosine similarity."""
        v = np.array(vector)
        norm = np.linalg.norm(v)
        if norm > 0:
            return (v / norm).tolist()
        return vector
        
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
    
    def embed_chunks(self, text: str, 
                    chunk_size: int = 512, 
                    chunk_overlap: int = 128,
                    separator: str = "\n") -> List[Dict]:
        """
        Split text into chunks and embed each chunk.
        
        Args:
            text: Text to split and embed
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks in characters
            separator: Preferred separator for chunks
            
        Returns:
            List of chunk dictionaries with text and embeddings
        """
        if not text or not isinstance(text, str):
            return []
            
        # Split text into chunks
        chunks = self._split_text(text, chunk_size, chunk_overlap, separator)
        
        # Generate embeddings for chunks
        if not chunks:
            return []
            
        embeddings = self.create_embeddings([chunk["text"] for chunk in chunks])
        
        # Add embeddings to chunks
        for i, embedding in enumerate(embeddings):
            chunks[i]["embedding"] = embedding
            chunks[i]["id"] = f"chunk_{i}"
            
        return chunks
    
    def _split_text(self, text: str, chunk_size: int, chunk_overlap: int, separator: str) -> List[Dict]:
        """Split text into overlapping chunks."""
        if not text:
            return []
            
        # If text is smaller than chunk size, return as is
        if len(text) <= chunk_size:
            return [{"text": text, "start": 0, "end": len(text)}]
            
        # Split by separator
        parts = text.split(separator)
        chunks = []
        current_chunk = ""
        current_start = 0
        last_end = 0
        
        for part in parts:
            # If adding the next part would exceed chunk size
            if len(current_chunk) + len(part) + len(separator) > chunk_size and current_chunk:
                # Add current chunk to results
                chunks.append({
                    "text": current_chunk, 
                    "start": current_start, 
                    "end": last_end
                })
                
                # Start new chunk with overlap
                overlap_start = max(0, last_end - chunk_overlap)
                current_chunk = text[overlap_start:last_end] + separator + part
                current_start = overlap_start
            else:
                # Add part to current chunk
                if current_chunk:
                    current_chunk += separator + part
                else:
                    current_chunk = part
                    current_start = 0
                    
            last_end = current_start + len(current_chunk)
            
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append({
                "text": current_chunk, 
                "start": current_start, 
                "end": last_end
            })
            
        return chunks

# Convenience functions for direct use without instantiating the class
def create_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Generate embeddings for a list of texts without instantiating a class"""
    generator = EnhancedEmbeddingGenerator(model=model)
    return generator.create_embeddings(texts)

def embed_document(document: Dict, text_field: str, 
                  embedding_field: str = "_embedding", 
                  model: str = "text-embedding-3-small") -> Dict:
    """Embed a single document without instantiating a class"""
    generator = EnhancedEmbeddingGenerator(model=model)
    result = generator.batch_embed_documents([document], text_field, embedding_field)
    return result[0] if result else document
    
def embed_and_chunk_text(text: str, 
                        chunk_size: int = 512, 
                        chunk_overlap: int = 128,
                        model: str = "text-embedding-3-small") -> List[Dict]:
    """Chunk text and embed each chunk without instantiating a class"""
    generator = EnhancedEmbeddingGenerator(model=model)
    return generator.embed_chunks(text, chunk_size, chunk_overlap)