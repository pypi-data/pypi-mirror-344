"""
Enhanced Vector Database Module

This module provides improved vector database connectors with support for:
1. Modern embedding models (OpenAI, custom)
2. Advanced metadata filtering
3. Hybrid search (semantic + keyword)
4. Optimized vector retrieval
"""

import logging
import os
import json
import re
import time
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Base class from vector_db
from .vector_db import VectorDBConnector

# Set up logging
logger = logging.getLogger(__name__)

class EnhancedVectorDB(VectorDBConnector):
    """
    Enhanced vector database with advanced features.
    """
    def __init__(self, 
                dimension: int = 1536,
                distance_metric: str = "cosine",
                embedding_model: str = "text-embedding-3-small",
                index_options: Optional[Dict] = None):
        """
        Initialize enhanced vector database.
        
        Args:
            dimension: Embedding dimension
            distance_metric: Distance metric (cosine, euclidean, dot)
            embedding_model: Embedding model identifier
            index_options: Additional options for index configuration
        """
        super().__init__()
        self.dimension = dimension
        
        if distance_metric not in ["cosine", "euclidean", "dot"]:
            raise ValueError(f"Unsupported distance metric: {distance_metric}")
            
        self.distance_metric = distance_metric
        self.embedding_model = embedding_model
        self.index_options = index_options or {}
        
        # Initialize data structures
        self.vectors = []
        self.metadata = []
        self.ids = []
        self.next_id = 0
        
        # Cache for common queries
        self.query_cache = {}
        self.max_cache_size = 100
        
        # Text search indexing
        self.text_index = {}  # Maps words to document IDs
        
        logger.info(f"Initialized EnhancedVectorDB with {embedding_model} model, dimension: {dimension}")
    
    def store_vectors(self, vectors: List[List[float]], metadata: List[Dict]) -> List[str]:
        """
        Store vectors in the database.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries
            
        Returns:
            List of IDs for stored vectors
        """
        if len(vectors) != len(metadata):
            raise ValueError("Number of vectors must match number of metadata items")
            
        # Generate IDs
        ids = [f"doc_{self.next_id + i}" for i in range(len(vectors))]
        self.next_id += len(vectors)
        
        # Store vectors and metadata
        self.vectors.extend(vectors)
        self.metadata.extend(metadata)
        self.ids.extend(ids)
        
        # Build text search index for hybrid search
        self._update_text_index(ids, metadata)
        
        # Clear query cache
        self.query_cache = {}
        
        return ids
        
    def add_documents(self, documents: List[Dict], embedding_field: str = "_embedding") -> List[str]:
        """
        Add documents containing embeddings to the vector database.
        
        Args:
            documents: List of documents with embeddings
            embedding_field: Field name containing embedding vector
            
        Returns:
            List of document IDs
        """
        # Extract vectors and metadata from documents
        vectors = []
        metadata = []
        
        for doc in documents:
            # Skip documents without embeddings
            if embedding_field not in doc:
                logger.warning(f"Document missing embedding field: {embedding_field}")
                continue
                
            # Extract embedding
            embedding = doc[embedding_field]
            vectors.append(embedding)
            
            # Create metadata without embedding field
            meta = doc.copy()
            meta.pop(embedding_field, None)
            metadata.append(meta)
        
        # Store vectors and metadata
        if not vectors:
            return []
            
        return self.store_vectors(vectors, metadata)
    
    def _update_text_index(self, ids: List[str], metadata: List[Dict]) -> None:
        """Update the text search index for hybrid search."""
        for doc_id, meta in zip(ids, metadata):
            # Index text content from metadata
            for field, value in meta.items():
                if isinstance(value, str):
                    # Tokenize text into words
                    words = re.findall(r'\w+', value.lower())
                    
                    # Add to index
                    for word in words:
                        if word not in self.text_index:
                            self.text_index[word] = set()
                        self.text_index[word].add(doc_id)
    
    def _vector_similarity(self, query_vector: List[float], document_vector: List[float]) -> float:
        """Calculate similarity between two vectors based on selected metric."""
        # Convert to numpy arrays
        q_vector = np.array(query_vector).reshape(1, -1)
        d_vector = np.array(document_vector).reshape(1, -1)
        
        if self.distance_metric == "cosine":
            # Higher is better for cosine
            return float(cosine_similarity(q_vector, d_vector)[0][0])
        elif self.distance_metric == "euclidean":
            # Lower is better for euclidean, so we negate
            return -float(np.linalg.norm(q_vector - d_vector))
        else:  # dot product
            # Higher is better for dot product
            return float(np.dot(q_vector, d_vector.T)[0][0])
    
    def search(self, 
              query_vector: List[float], 
              top_k: int = 10, 
              filters: Optional[Dict] = None,
              hybrid_search_text: Optional[str] = None,
              hybrid_alpha: float = 0.5) -> List[Dict]:
        """
        Enhanced search for similar vectors with advanced filtering and hybrid search.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return 
            filters: Metadata filters in format: 
                     {'attribute': value} or 
                     {'attribute': {'$gt': value}} (greater than)
                     {'attribute': {'$lt': value}} (less than)
                     {'attribute': {'$in': [value1, value2]}} (in list)
            hybrid_search_text: Optional text for hybrid search (combines vector and text search)
            hybrid_alpha: Weight for hybrid search (0 = vector only, 1 = text only)
            
        Returns:
            List of search results with scores and metadata
        """
        # Ensure top_k is an integer
        top_k = int(top_k)
        
        if not self.vectors:
            return []
        
        # Check cache for identical query
        cache_key = (
            tuple(query_vector), 
            top_k,
            json.dumps(filters) if filters else None,
            hybrid_search_text,
            hybrid_alpha
        )
        
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]
            
        # Get matching document IDs from text search if hybrid search is enabled
        matching_text_ids = set()
        text_scores = {}
        
        if hybrid_search_text:
            # Extract search words
            search_words = re.findall(r'\w+', hybrid_search_text.lower())
            
            # Get document IDs containing any search word
            for word in search_words:
                if word in self.text_index:
                    matching_text_ids.update(self.text_index[word])
                    
            # Calculate text match scores (simple word frequency)
            for doc_id in matching_text_ids:
                idx = self.ids.index(doc_id)
                doc_meta = self.metadata[idx]
                
                # Count word matches in document metadata
                word_matches = 0
                for field, value in doc_meta.items():
                    if isinstance(value, str):
                        for word in search_words:
                            # Count case-insensitive matches
                            word_matches += value.lower().count(word.lower())
                
                # Store text match score
                text_scores[doc_id] = word_matches / max(1, len(search_words))
        
        # Calculate vector similarities and apply filters
        vector_scores = []
        
        for i, vector in enumerate(self.vectors):
            doc_id = self.ids[i]
            doc_meta = self.metadata[i]
            
            # Apply filters if provided
            if filters and not self._apply_filters(doc_meta, filters):
                continue
                
            # Calculate vector similarity
            vector_score = self._vector_similarity(query_vector, vector)
            
            # Calculate hybrid score if hybrid search is enabled
            final_score = vector_score
            if hybrid_search_text:
                text_score = text_scores.get(doc_id, 0)
                final_score = (1 - hybrid_alpha) * vector_score + hybrid_alpha * text_score
            
            vector_scores.append((final_score, i))
        
        # Sort by score (descending)
        vector_scores.sort(reverse=True)
        
        # Format results
        results = []
        for score, idx in vector_scores[:top_k]:
            result = {
                "id": self.ids[idx],
                "score": float(score),
                "metadata": self.metadata[idx]
            }
            results.append(result)
        
        # Cache results if not too many entries
        if len(self.query_cache) < self.max_cache_size:
            self.query_cache[cache_key] = results
            
        return results
    
    def _apply_filters(self, metadata: Dict, filters: Dict) -> bool:
        """Apply filters to metadata and return whether it matches."""
        for key, filter_value in filters.items():
            # Handle dot notation for nested objects
            if '.' in key:
                parts = key.split('.')
                value = metadata
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        # Path doesn't exist
                        return False
            else:
                # Handle simple key
                if key not in metadata:
                    return False
                value = metadata[key]
                
            # Handle different filter types
            if isinstance(filter_value, dict):
                # Advanced filter operators
                for op, op_value in filter_value.items():
                    if op == '$gt' and not (value > op_value):
                        return False
                    elif op == '$lt' and not (value < op_value):
                        return False
                    elif op == '$gte' and not (value >= op_value):
                        return False
                    elif op == '$lte' and not (value <= op_value):
                        return False
                    elif op == '$in' and value not in op_value:
                        return False
                    elif op == '$nin' and value in op_value:
                        return False
                    elif op == '$contains' and not (op_value in value if isinstance(value, str) else False):
                        return False
            else:
                # Simple equality filter
                if value != filter_value:
                    return False
                    
        return True
    
    def delete(self, ids: List[str]) -> bool:
        """
        Delete vectors by ID.
        
        Args:
            ids: List of vector IDs to delete
            
        Returns:
            Success status
        """
        if not ids:
            return True
            
        # Convert IDs to set for efficient lookup
        id_set = set(ids)
        
        # Create new lists excluding deleted IDs
        new_vectors = []
        new_metadata = []
        new_ids = []
        
        for i, id_str in enumerate(self.ids):
            if id_str not in id_set:
                new_vectors.append(self.vectors[i])
                new_metadata.append(self.metadata[i])
                new_ids.append(id_str)
                
        # Update instance variables
        self.vectors = new_vectors
        self.metadata = new_metadata
        self.ids = new_ids
        
        # Rebuild text index
        self.text_index = {}
        self._update_text_index(new_ids, new_metadata)
        
        # Clear query cache
        self.query_cache = {}
        
        return True
    
    def search_by_text(self, query_text: str, top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search documents by text without requiring a vector.
        Uses any available text vectors if available, otherwise returns keyword matches.
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of search results with scores and metadata
        """
        # Extract search words
        search_words = re.findall(r'\w+', query_text.lower())
        if not search_words:
            return []
            
        # Get document IDs containing any search word
        matching_ids = set()
        for word in search_words:
            if word in self.text_index:
                matching_ids.update(self.text_index[word])
                
        # Calculate text match scores and apply filters
        matches = []
        for doc_id in matching_ids:
            idx = self.ids.index(doc_id)
            doc_meta = self.metadata[idx]
            
            # Apply filters if provided
            if filters and not self._apply_filters(doc_meta, filters):
                continue
            
            # Count word matches in document metadata
            word_matches = 0
            word_occurrences = 0
            for field, value in doc_meta.items():
                if isinstance(value, str):
                    for word in search_words:
                        count = value.lower().count(word.lower())
                        if count > 0:
                            word_matches += 1
                            word_occurrences += count
            
            # Calculate score based on number of matching words and occurrences
            match_ratio = word_matches / len(search_words)
            score = match_ratio * (1 + min(1, word_occurrences / 10))
            matches.append((score, idx))
            
        # Sort by score (descending)
        matches.sort(reverse=True)
        
        # Format results
        results = []
        for score, idx in matches[:top_k]:
            result = {
                "id": self.ids[idx],
                "score": float(score),
                "metadata": self.metadata[idx]
            }
            results.append(result)
            
        return results

    def save_index(self, filepath: str) -> bool:
        """
        Save the vector index and metadata to disk.
        
        Args:
            filepath: Path to save index
            
        Returns:
            Success status
        """
        try:
            # Save vectors, metadata, and IDs
            with open(f"{filepath}.json", "w") as f:
                json.dump({
                    "dimension": self.dimension,
                    "distance_metric": self.distance_metric,
                    "embedding_model": self.embedding_model,
                    "index_options": self.index_options,
                    "next_id": self.next_id,
                    "vectors": self.vectors,
                    "metadata": self.metadata,
                    "ids": self.ids
                }, f)
                
            return True
        except Exception as e:
            logger.error(f"Error saving enhanced vector index: {str(e)}")
            return False
    
    @classmethod
    def load_index(cls, filepath: str) -> "EnhancedVectorDB":
        """
        Load vector index and metadata from disk.
        
        Args:
            filepath: Path to load index from
            
        Returns:
            Loaded EnhancedVectorDB instance
        """
        try:
            # Load data
            with open(f"{filepath}.json", "r") as f:
                data = json.load(f)
                
            # Create instance
            instance = cls(
                dimension=data["dimension"],
                distance_metric=data["distance_metric"],
                embedding_model=data["embedding_model"],
                index_options=data["index_options"]
            )
            
            # Set data
            instance.vectors = data["vectors"]
            instance.metadata = data["metadata"]
            instance.ids = data["ids"]
            instance.next_id = data["next_id"]
            
            # Rebuild text index
            instance._update_text_index(instance.ids, instance.metadata)
            
            return instance
        except Exception as e:
            logger.error(f"Error loading enhanced vector index: {str(e)}")
            raise

# Create EnhancedVectorDB instance
def create_enhanced_vector_db(
    dimension: int = 1536,
    distance_metric: str = "cosine", 
    embedding_model: str = "text-embedding-3-small",
    index_options: Optional[Dict] = None
) -> EnhancedVectorDB:
    """
    Create an enhanced vector database.
    
    Args:
        dimension: Embedding dimension
        distance_metric: Distance metric (cosine, euclidean, dot)
        embedding_model: Embedding model identifier
        index_options: Additional options for index configuration
        
    Returns:
        EnhancedVectorDB instance
    """
    return EnhancedVectorDB(
        dimension=dimension,
        distance_metric=distance_metric,
        embedding_model=embedding_model,
        index_options=index_options
    )

class HybridSearchEngine:
    """
    Hybrid search engine combining vector search and keyword search.
    """
    def __init__(self, vector_db: EnhancedVectorDB):
        """
        Initialize hybrid search engine.
        
        Args:
            vector_db: EnhancedVectorDB instance
        """
        self.vector_db = vector_db
        self.logger = logging.getLogger(__name__)
    
    def search(self, 
              query_text: str, 
              query_vector: Optional[List[float]] = None,
              top_k: int = 10, 
              filters: Optional[Dict] = None,
              hybrid_alpha: float = 0.5) -> List[Dict]:
        """
        Perform hybrid search using both vector and keyword search.
        
        Args:
            query_text: Text query
            query_vector: Optional query vector (if None, only text search is used)
            top_k: Number of results to return
            filters: Optional metadata filters
            hybrid_alpha: Weight for hybrid search (0 = vector only, 1 = text only)
            
        Returns:
            List of search results with scores and metadata
        """
        if query_vector is not None:
            # Hybrid search with vector
            return self.vector_db.search(
                query_vector=query_vector,
                top_k=top_k,
                filters=filters,
                hybrid_search_text=query_text,
                hybrid_alpha=hybrid_alpha
            )
        else:
            # Text-only search
            return self.vector_db.search_by_text(
                query_text=query_text,
                top_k=top_k,
                filters=filters
            )