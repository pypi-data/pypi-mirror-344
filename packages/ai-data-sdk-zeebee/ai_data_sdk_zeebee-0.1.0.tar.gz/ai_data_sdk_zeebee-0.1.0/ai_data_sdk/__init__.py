"""
AI Data SDK
===========

A comprehensive SDK for standardizing, processing, embedding, and retrieving 
data for AI applications.

Modules:
    - ingestion: Data ingestion from various sources
    - quality: Data validation and quality checks
    - metadata: Metadata management for AI data
    - embedding: Text embedding generation
    - pii: PII detection and masking
    - vector_db: Vector database connectors
    - feedback: Drift detection and user feedback

Usage:
    from ai_data_sdk import ingestion, embedding, vector_db
    
    # Ingest data
    data = ingestion.load_from_json("data.json")
    
    # Generate embeddings
    embeddings = embedding.create_embeddings(data)
    
    # Store in vector DB
    vector_db.store_vectors(embeddings)
"""

__version__ = '0.1.0'

from . import ingestion
from . import quality
from . import metadata
from . import embedding
from . import pii
from . import vector_db
from . import feedback

# For simplified imports
from .ingestion import DataIngester
from .quality import DataValidator
from .metadata import MetadataManager
from .embedding import EmbeddingGenerator
from .pii import PIIDetector
from .vector_db import VectorDBConnector
from .feedback import FeedbackCollector
