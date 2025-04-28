"""
Vector Database Connector Module

This module provides connectors for various vector databases including
in-memory database for testing purposes. 
FAISS support is temporarily disabled due to compatibility issues.
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import numpy as np
# import faiss - temporarily disabled

class VectorDBConnector:
    """
    Base class for vector database connectors.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def store_vectors(self, vectors: List[List[float]], metadata: List[Dict]) -> List[str]:
        """
        Store vectors in the database.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries
            
        Returns:
            List of IDs for stored vectors
        """
        raise NotImplementedError("Subclasses must implement store_vectors")
    
    def search(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of search results with scores and metadata
        """
        raise NotImplementedError("Subclasses must implement search")
    
    def delete(self, ids: List[str]) -> bool:
        """
        Delete vectors by ID.
        
        Args:
            ids: List of vector IDs to delete
            
        Returns:
            Success status
        """
        raise NotImplementedError("Subclasses must implement delete")

class FaissVectorDB(VectorDBConnector):
    """
    FAISS vector database connector for local in-memory vector search.
    """
    def __init__(self, dimension: int = 1536, index_type: str = "L2"):
        """
        Initialize FAISS vector database.
        CURRENTLY DISABLED - Using in-memory database instead
        
        Args:
            dimension: Embedding dimension
            index_type: FAISS index type (L2, IP, Cosine)
        """
        super().__init__()
        self.dimension = dimension
        self.index_type = index_type
        self.logger.warning("FAISS is currently disabled. Using in-memory database instead.")
        
        # FAISS index creation is disabled
        # Create empty data structures
        self.metadata = []
        self.ids = []
        self.next_id = 0
            
        # Store metadata separately
        self.metadata = []
        self.ids = []
        self.next_id = 0
        
    def store_vectors(self, vectors: List[List[float]], metadata: List[Dict]) -> List[str]:
        """
        Store vectors in FAISS.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries
            
        Returns:
            List of IDs for stored vectors
        """
        if len(vectors) != len(metadata):
            raise ValueError("Number of vectors must match number of metadata items")
            
        # Convert to numpy array
        np_vectors = np.array(vectors).astype('float32')
        
        # Normalize for cosine similarity if needed
        if self.index_type == "Cosine":
            faiss.normalize_L2(np_vectors)
            
        # Generate IDs
        ids = [str(self.next_id + i) for i in range(len(vectors))]
        self.next_id += len(vectors)
        
        # Add to FAISS index
        self.index.add(np_vectors)
        
        # Store metadata and IDs
        self.metadata.extend(metadata)
        self.ids.extend(ids)
        
        return ids
    
    def search(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        """
        Search for similar vectors in FAISS.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of search results with scores and metadata
        """
        # Ensure top_k is an integer
        top_k = int(top_k)
        
        # Convert to numpy array
        np_query = np.array([query_vector]).astype('float32')
        
        # Normalize for cosine similarity if needed
        if self.index_type == "Cosine":
            faiss.normalize_L2(np_query)
            
        # Search
        distances, indices = self.index.search(np_query, min(top_k, len(self.metadata)))
        
        # Format results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                result = {
                    "id": self.ids[idx],
                    "score": float(distance),
                    "metadata": self.metadata[idx]
                }
                results.append(result)
                
        return results
    
    def delete(self, ids: List[str]) -> bool:
        """
        Delete vectors by ID.
        
        Note: FAISS doesn't support direct deletion from IndexFlat.
        This implementation creates a new index without the deleted vectors.
        
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
        new_metadata = []
        new_ids = []
        keep_indices = []
        
        for i, id_str in enumerate(self.ids):
            if id_str not in id_set:
                new_metadata.append(self.metadata[i])
                new_ids.append(id_str)
                keep_indices.append(i)
                
        # Recreate index with kept vectors
        if keep_indices:
            # Create new index
            if self.index_type == "L2":
                new_index = faiss.IndexFlatL2(self.dimension)
            elif self.index_type in ["IP", "Cosine"]:
                new_index = faiss.IndexFlatIP(self.dimension)
            
            # Get vectors to keep
            keep_indices = np.array(keep_indices)
            
            # Extract vectors from original index
            vectors = np.zeros((len(keep_indices), self.dimension), dtype='float32')
            for i, idx in enumerate(keep_indices):
                vector = np.zeros((1, self.dimension), dtype='float32')
                self.index.reconstruct(idx, vector[0])
                vectors[i] = vector[0]
                
            # Add vectors to new index
            new_index.add(vectors)
            
            # Update instance variables
            self.index = new_index
            self.metadata = new_metadata
            self.ids = new_ids
        else:
            # All vectors deleted, reset index
            if self.index_type == "L2":
                self.index = faiss.IndexFlatL2(self.dimension)
            elif self.index_type in ["IP", "Cosine"]:
                self.index = faiss.IndexFlatIP(self.dimension)
                
            self.metadata = []
            self.ids = []
            
        return True
    
    def save_index(self, filepath: str) -> bool:
        """
        Save FAISS index and metadata to disk.
        
        Args:
            filepath: Path to save index
            
        Returns:
            Success status
        """
        try:
            # Save FAISS index
            faiss.write_index(self.index, f"{filepath}.index")
            
            # Save metadata and IDs
            with open(f"{filepath}.meta", "w") as f:
                json.dump({
                    "metadata": self.metadata,
                    "ids": self.ids,
                    "next_id": self.next_id,
                    "dimension": self.dimension,
                    "index_type": self.index_type
                }, f)
                
            return True
        except Exception as e:
            self.logger.error(f"Error saving index: {str(e)}")
            return False
    
    @classmethod
    def load_index(cls, filepath: str) -> "FaissVectorDB":
        """
        Load FAISS index and metadata from disk.
        
        Args:
            filepath: Path to load index from
            
        Returns:
            Loaded FaissVectorDB instance
        """
        try:
            # Load metadata and IDs
            with open(f"{filepath}.meta", "r") as f:
                meta_data = json.load(f)
                
            # Create instance
            instance = cls(dimension=meta_data["dimension"], index_type=meta_data["index_type"])
            
            # Load FAISS index
            instance.index = faiss.read_index(f"{filepath}.index")
            
            # Set metadata and IDs
            instance.metadata = meta_data["metadata"]
            instance.ids = meta_data["ids"]
            instance.next_id = meta_data["next_id"]
            
            return instance
        except Exception as e:
            logging.error(f"Error loading index: {str(e)}")
            raise

class MemoryVectorDB(VectorDBConnector):
    """
    Simple in-memory vector database for testing and small datasets.
    """
    def __init__(self, distance_metric: str = "cosine"):
        """
        Initialize in-memory vector database.
        
        Args:
            distance_metric: Distance metric (cosine, euclidean, dot)
        """
        super().__init__()
        self.vectors = []
        self.metadata = []
        self.ids = []
        self.next_id = 0
        
        if distance_metric not in ["cosine", "euclidean", "dot"]:
            raise ValueError(f"Unsupported distance metric: {distance_metric}")
            
        self.distance_metric = distance_metric
    
    def store_vectors(self, vectors: List[List[float]], metadata: List[Dict]) -> List[str]:
        """
        Store vectors in memory.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries
            
        Returns:
            List of IDs for stored vectors
        """
        if len(vectors) != len(metadata):
            raise ValueError("Number of vectors must match number of metadata items")
            
        # Generate IDs
        ids = [str(self.next_id + i) for i in range(len(vectors))]
        self.next_id += len(vectors)
        
        # Store vectors and metadata
        self.vectors.extend(vectors)
        self.metadata.extend(metadata)
        self.ids.extend(ids)
        
        return ids
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        # Convert to float to ensure all elements are numeric
        try:
            a_float = [float(x) for x in a]
            b_float = [float(x) for x in b]
        except ValueError:
            # Handle case where vectors contain non-numeric values
            a_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in a]
            b_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in b]
        
        a_norm = np.sqrt(sum(x*x for x in a_float))
        b_norm = np.sqrt(sum(x*x for x in b_float))
        
        if a_norm == 0 or b_norm == 0:
            return 0
            
        dot_product = sum(x*y for x, y in zip(a_float, b_float))
        return dot_product / (a_norm * b_norm)
    
    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        """Calculate Euclidean distance between two vectors."""
        # Convert to float to ensure all elements are numeric
        try:
            a_float = [float(x) for x in a]
            b_float = [float(x) for x in b]
        except ValueError:
            # Handle case where vectors contain non-numeric values
            a_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in a]
            b_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in b]
        return np.sqrt(sum((x - y) ** 2 for x, y in zip(a_float, b_float)))
    
    def _dot_product(self, a: List[float], b: List[float]) -> float:
        """Calculate dot product between two vectors."""
        # Convert to float to ensure all elements are numeric
        try:
            a_float = [float(x) for x in a]
            b_float = [float(x) for x in b]
        except ValueError:
            # Handle case where vectors contain non-numeric values
            a_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in a]
            b_float = [float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else 0.0 for x in b]
        return sum(x*y for x, y in zip(a_float, b_float))
    
    def search(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        """
        Search for similar vectors in memory.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of search results with scores and metadata
        """
        # Ensure top_k is an integer
        top_k = int(top_k)
        
        if not self.vectors:
            return []
            
        # Calculate similarities/distances
        scores = []
        for vector in self.vectors:
            if self.distance_metric == "cosine":
                # Higher is better for cosine
                score = self._cosine_similarity(query_vector, vector)
            elif self.distance_metric == "euclidean":
                # Lower is better for Euclidean, so we negate
                score = -self._euclidean_distance(query_vector, vector)
            else:  # dot product
                # Higher is better for dot product
                score = self._dot_product(query_vector, vector)
                
            scores.append(score)
            
        # Sort by score (descending)
        results_with_scores = list(zip(scores, range(len(self.vectors))))
        results_with_scores.sort(reverse=True)
        
        # Format top_k results
        results = []
        for score, idx in results_with_scores[:top_k]:
            result = {
                "id": self.ids[idx],
                "score": float(score),
                "metadata": self.metadata[idx]
            }
            results.append(result)
            
        return results
    
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
        
        return True

# Factory function to create appropriate vector database connector
def create_vector_db(db_type: str = "memory", **kwargs) -> VectorDBConnector:
    """
    Create a vector database connector based on the specified type.
    
    Args:
        db_type: Type of vector database (memory or faiss - though faiss is currently disabled)
        **kwargs: Additional arguments for the specific connector
        
    Returns:
        VectorDBConnector instance
    """
    # For now, we're using the in-memory database regardless of the requested type
    # due to compatibility issues with FAISS
    return MemoryVectorDB(**kwargs)

class VectorDB:
    """
    Main vector database interface class.
    
    This class provides a simplified interface to the underlying vector database connectors.
    It handles document management, metadata, and vector operations.
    """
    def __init__(self, db_type: str = "memory", **kwargs):
        """
        Initialize vector database.
        
        Args:
            db_type: Type of vector database (memory or faiss)
            **kwargs: Additional arguments for the specific connector
        """
        self.logger = logging.getLogger(__name__)
        self.connector = create_vector_db(db_type, **kwargs)
        self.documents = {}  # Store original documents by ID
        
    def add_documents(self, documents: List[Dict], embedding_field: str = "_embedding") -> List[str]:
        """
        Add documents to the vector database.
        
        Args:
            documents: List of document dictionaries with embeddings
            embedding_field: Field name containing the embedding vector
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
            
        # Extract vectors and metadata
        vectors = []
        metadata = []
        
        for doc in documents:
            if embedding_field not in doc:
                raise ValueError(f"Document missing embedding field: {embedding_field}")
                
            # Extract vector
            vector = doc[embedding_field]
            
            # Create metadata (document without the embedding vector)
            meta = {k: v for k, v in doc.items() if k != embedding_field}
            
            vectors.append(vector)
            metadata.append(meta)
            
        # Store in vector database
        ids = self.connector.store_vectors(vectors, metadata)
        
        # Store original documents
        for id_str, doc in zip(ids, documents):
            self.documents[id_str] = doc
            
        return ids
        
    def search(self, query_vector: List[float], top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar documents.
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of search results with scores and metadata
        """
        # Ensure top_k is an integer
        top_k = int(top_k)
        self.logger.debug(f"VectorDB search called with top_k: {top_k}, type: {type(top_k)}")
        
        # Basic search
        self.logger.debug(f"Calling connector.search with top_k: {top_k}")
        results = self.connector.search(query_vector, top_k)
        
        # Apply filters if provided
        if filters is not None:
            filtered_results = []
            for result in results:
                # Check if all filter criteria match
                if all(result["metadata"].get(k) == v for k, v in filters.items()):
                    filtered_results.append(result)
            results = filtered_results
            
        return results
        
    def delete(self, ids: List[str]) -> bool:
        """
        Delete documents by ID.
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            Success status
        """
        # Delete from vector database
        success = self.connector.delete(ids)
        
        # Delete from documents store
        for id_str in ids:
            if id_str in self.documents:
                del self.documents[id_str]
                
        return success
        
    def get_document(self, id_str: str) -> Optional[Dict]:
        """
        Get original document by ID.
        
        Args:
            id_str: Document ID
            
        Returns:
            Original document or None if not found
        """
        return self.documents.get(id_str)
