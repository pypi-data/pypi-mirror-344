"""
AI Data SDK Enhanced Module

This module integrates all enhanced components of the AI Data SDK
to provide a unified interface for processing, embedding, storing, 
and retrieving data.
"""

import logging
import json
import time
from typing import List, Dict, Any, Optional, Union, Callable, Set, Tuple

# Import enhanced modules
from .embedding_enhanced import EnhancedEmbeddingGenerator, embed_and_chunk_text
from .vector_db_enhanced import EnhancedVectorDB, HybridSearchEngine
from .quality_enhanced import DataQualityValidator, DatasetAnalyzer
from .ingestion_enhanced import EnhancedDataIngester, WebCrawler
from .pii import PIIDetector

# Set up logging
logger = logging.getLogger(__name__)

class EnhancedAIDataPipeline:
    """
    Enhanced AI data processing pipeline integrating all modules.
    """
    def __init__(self, 
                embedding_model: str = "text-embedding-3-small",
                vector_dimension: int = 1536,
                vector_distance: str = "cosine",
                quality_schema: Optional[Dict] = None,
                text_field: str = "text",
                pii_detection: bool = True):
        """
        Initialize enhanced AI data pipeline.
        
        Args:
            embedding_model: Model name for embeddings
            vector_dimension: Embedding vector dimension
            vector_distance: Distance metric for vector search
            quality_schema: Optional data quality JSON schema
            text_field: Default field name for text content
            pii_detection: Whether to enable PII detection
        """
        self.text_field = text_field
        
        # Initialize components
        self.embedding_generator = EnhancedEmbeddingGenerator(
            model=embedding_model,
            dimensions=vector_dimension
        )
        
        self.vector_db = EnhancedVectorDB(
            dimension=vector_dimension,
            distance_metric=vector_distance,
            embedding_model=embedding_model
        )
        
        self.search_engine = HybridSearchEngine(
            vector_db=self.vector_db
        )
        
        self.data_ingester = EnhancedDataIngester(
            preprocessors=[
                self._clean_text
            ]
        )
        
        self.quality_validator = DataQualityValidator(
            schema=quality_schema
        )
        
        self.dataset_analyzer = DatasetAnalyzer(
            text_field=text_field
        )
        
        if pii_detection:
            self.pii_detector = PIIDetector()
        else:
            self.pii_detector = None
            
        self.logger = logger
        
        logger.info(f"Initialized EnhancedAIDataPipeline with {embedding_model} model")
    
    def process_data(self, 
                   source: Any,
                   chunk: bool = False,
                   chunk_size: int = 1000,
                   chunk_overlap: int = 200,
                   validate: bool = True,
                   detect_pii: bool = False,
                   mask_pii: bool = False) -> Dict:
        """
        Process data from source through the entire pipeline.
        
        Args:
            source: Data source (file, URL, string, etc.)
            chunk: Whether to chunk documents
            chunk_size: Size of chunks if chunking
            chunk_overlap: Overlap between chunks
            validate: Whether to validate document quality
            detect_pii: Whether to detect PII
            mask_pii: Whether to mask detected PII
            
        Returns:
            Processing results with document IDs and stats
        """
        start_time = time.time()
        results = {
            "success": True,
            "document_count": 0,
            "processed_count": 0,
            "embedding_count": 0,
            "document_ids": [],
            "errors": [],
            "quality_score": None,
            "pii_detected": False
        }
        
        try:
            # Step 1: Ingest data
            self.logger.info(f"Ingesting data from source")
            if chunk:
                documents = self.data_ingester.load_and_chunk(
                    source, chunk_size, chunk_overlap, self.text_field
                )
            else:
                documents = self.data_ingester.load_from_source(
                    source, text_field=self.text_field
                )
                
            if not documents:
                results["success"] = False
                results["errors"].append("No documents extracted from source")
                return results
                
            results["document_count"] = len(documents)
            self.logger.info(f"Ingested {len(documents)} documents")
            
            # Step 2: Validate quality if requested
            if validate:
                self.logger.info("Validating document quality")
                quality_results = self.quality_validator.validate_dataset(documents)
                results["quality_results"] = quality_results
                
                if not quality_results["valid"]:
                    results["warnings"] = [
                        f"Quality validation found {quality_results['error_count']} documents with errors"
                    ]
                
                # Calculate average quality score
                quality_scores = [
                    self.quality_validator.calculate_quality_score(doc)
                    for doc in documents
                ]
                results["quality_score"] = sum(quality_scores) / len(quality_scores)
            
            # Step 3: Detect and mask PII if requested
            if detect_pii and self.pii_detector:
                self.logger.info("Detecting PII in documents")
                pii_found = False
                
                for doc in documents:
                    # Process text fields
                    for field, value in doc.items():
                        if isinstance(value, str) and len(value) > 10:
                            # Detect PII
                            pii_instances = self.pii_detector.detect_pii(value)
                            
                            if pii_instances:
                                pii_found = True
                                # Add PII metadata to document
                                if "pii_detected" not in doc:
                                    doc["pii_detected"] = {}
                                doc["pii_detected"][field] = pii_instances
                                
                                # Mask PII if requested
                                if mask_pii:
                                    masked_text = self.pii_detector.mask_pii(value)
                                    doc[field] = masked_text
                
                results["pii_detected"] = pii_found
            
            # Step 4: Generate embeddings
            self.logger.info("Generating embeddings")
            embedded_documents = self.embedding_generator.batch_embed_documents(
                documents, self.text_field
            )
            
            # Step 5: Store in vector database
            self.logger.info("Storing in vector database")
            doc_ids = self.vector_db.add_documents(embedded_documents)
            
            results["processed_count"] = len(embedded_documents)
            results["embedding_count"] = len(doc_ids)
            results["document_ids"] = doc_ids
            
            # Record timing
            results["processing_time"] = time.time() - start_time
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in data pipeline: {str(e)}")
            results["success"] = False
            results["errors"].append(str(e))
            return results
    
    def search(self, 
              query: str,
              query_vector: Optional[List[float]] = None,
              top_k: int = 10,
              filters: Optional[Dict] = None,
              hybrid_alpha: float = 0.5) -> List[Dict]:
        """
        Search for documents using text query or vector.
        
        Args:
            query: Text query
            query_vector: Optional pre-computed query vector
            top_k: Number of results to return
            filters: Optional metadata filters
            hybrid_alpha: Weight for hybrid search (0=vector only, 1=text only)
            
        Returns:
            Search results with scores and metadata
        """
        try:
            # Generate query vector if not provided
            if not query_vector and query:
                query_vectors = self.embedding_generator.create_embeddings([query])
                query_vector = query_vectors[0] if query_vectors else None
            
            # Perform search
            if query_vector:
                # Vector or hybrid search
                results = self.search_engine.search(
                    query_text=query,
                    query_vector=query_vector,
                    top_k=top_k,
                    filters=filters,
                    hybrid_alpha=hybrid_alpha
                )
            else:
                # Text-only search
                results = self.vector_db.search_by_text(
                    query_text=query,
                    top_k=top_k,
                    filters=filters
                )
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error in search: {str(e)}")
            return []
    
    def process_website(self, 
                      url: str,
                      max_pages: int = 10, 
                      max_depth: int = 2,
                      chunk: bool = True,
                      chunk_size: int = 1000) -> Dict:
        """
        Process content from a website.
        
        Args:
            url: Website URL
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum crawl depth
            chunk: Whether to chunk documents
            chunk_size: Size of chunks if chunking
            
        Returns:
            Processing results
        """
        try:
            # Crawl website
            self.logger.info(f"Crawling website: {url}")
            crawler = WebCrawler(
                max_pages=max_pages,
                max_depth=max_depth
            )
            
            documents = crawler.crawl(url, self.text_field)
            
            if not documents:
                return {
                    "success": False,
                    "errors": ["No content extracted from website"]
                }
                
            # Process documents
            if chunk:
                # Split documents into chunks
                chunked_docs = []
                for doc in documents:
                    text = doc.get(self.text_field, "")
                    if text:
                        chunks = self._split_into_chunks(text, chunk_size, metadata=doc)
                        chunked_docs.extend(chunks)
                    else:
                        chunked_docs.append(doc)
                        
                documents = chunked_docs
            
            # Generate embeddings
            embedded_documents = self.embedding_generator.batch_embed_documents(
                documents, self.text_field
            )
            
            # Store in vector database
            doc_ids = self.vector_db.add_documents(embedded_documents)
            
            return {
                "success": True,
                "page_count": len(crawler.visited_urls),
                "document_count": len(documents),
                "embedding_count": len(doc_ids),
                "document_ids": doc_ids
            }
            
        except Exception as e:
            self.logger.error(f"Error processing website: {str(e)}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and HTML tags."""
        # Replace multiple spaces with single space
        text = text.replace('\t', ' ')
        text = text.replace('\r', '\n')
        text = text.replace('\u00a0', ' ')  # Non-breaking space
        text = text.replace('\u2019', "'")  # Smart quote
        
        # Remove extra line breaks
        text = text.replace('\n\n\n', '\n\n')
        
        # Remove any remaining HTML tags
        text = text.replace('<br>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('&nbsp;', ' ')
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _split_into_chunks(self, text: str, chunk_size: int, metadata: Dict = None) -> List[Dict]:
        """Split text into chunks with metadata."""
        # Check if text is small enough to be a single chunk
        if len(text) <= chunk_size:
            return [{**metadata, self.text_field: text}]
            
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # If adding paragraph would exceed chunk size and we have content
            if len(current_chunk) + len(para) + 2 > chunk_size and current_chunk:
                # Create chunk with metadata
                chunk_doc = {self.text_field: current_chunk}
                if metadata:
                    for key, value in metadata.items():
                        if key != self.text_field:
                            chunk_doc[key] = value
                            
                # Add chunk index
                chunk_doc["chunk_index"] = len(chunks)
                chunks.append(chunk_doc)
                
                # Start new chunk
                current_chunk = para
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
        
        # Add final chunk if not empty
        if current_chunk:
            chunk_doc = {self.text_field: current_chunk}
            if metadata:
                for key, value in metadata.items():
                    if key != self.text_field:
                        chunk_doc[key] = value
                        
            # Add chunk index
            chunk_doc["chunk_index"] = len(chunks)
            chunks.append(chunk_doc)
            
        # Add total chunks to all chunks
        for chunk in chunks:
            chunk["chunk_count"] = len(chunks)
            
        return chunks

# Helper functions
def create_pipeline(embedding_model: str = "text-embedding-3-small") -> EnhancedAIDataPipeline:
    """Create an enhanced AI data pipeline."""
    return EnhancedAIDataPipeline(embedding_model=embedding_model)

def process_data_source(source: Any, 
                      embedding_model: str = "text-embedding-3-small", 
                      chunk: bool = False) -> Dict:
    """Process data from a source without instantiating a pipeline."""
    pipeline = EnhancedAIDataPipeline(embedding_model=embedding_model)
    return pipeline.process_data(source, chunk=chunk)

def search_documents(query: str, 
                   top_k: int = 10, 
                   embedding_model: str = "text-embedding-3-small") -> List[Dict]:
    """Search documents without instantiating a pipeline."""
    pipeline = EnhancedAIDataPipeline(embedding_model=embedding_model)
    return pipeline.search(query, top_k=top_k)