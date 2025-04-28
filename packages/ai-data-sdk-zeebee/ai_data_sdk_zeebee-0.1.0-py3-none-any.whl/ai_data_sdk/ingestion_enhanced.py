"""
Enhanced Data Ingestion Module

This module provides advanced utilities for ingesting and preprocessing data 
from various sources including binary files, web content, and structured documents.
"""

import json
import logging
import re
import csv
import os
import hashlib
import mimetypes
from typing import List, Dict, Any, Union, Optional, Callable, TextIO, BinaryIO, Set, Tuple
from pathlib import Path
import urllib.request
import urllib.parse
from datetime import datetime
import concurrent.futures
import trafilatura
import requests

from .validation import InputValidationError

# Set up logging
logger = logging.getLogger(__name__)

class EnhancedDataIngester:
    """
    Enhanced class for ingesting data from various sources with advanced preprocessing.
    """
    def __init__(self, 
                preprocessors: Optional[List[Callable]] = None,
                max_workers: int = 4,
                chunk_size: int = 1000):
        """
        Initialize enhanced data ingester.
        
        Args:
            preprocessors: Optional list of preprocessing functions to apply to text data
            max_workers: Maximum number of concurrent workers for parallel processing
            chunk_size: Size of chunks for batch processing
        """
        self.preprocessors = preprocessors or []
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.logger = logger
        
        # Initialize content type handlers
        self.content_type_handlers = {
            "application/json": self._process_json,
            "text/csv": self._process_csv,
            "text/plain": self._process_text,
            "text/markdown": self._process_text,
            "text/html": self._process_html,
            "application/pdf": self._process_unsupported  # Placeholder for PDF support
        }
    
    def load_from_source(self, source: Union[str, Path, TextIO, Dict], 
                       content_type: Optional[str] = None,
                       text_field: str = 'text') -> List[Dict]:
        """
        Load data from any source with automatic content type detection.
        
        Args:
            source: Source data (file path, URL, string, file-like object, or dictionary)
            content_type: Optional content type hint (MIME type)
            text_field: Field name containing the text to process
            
        Returns:
            List of document dictionaries
        """
        try:
            # Handle different source types
            content = None
            detected_type = content_type
            file_path = None
            
            # URLs - download content
            if isinstance(source, str) and (source.startswith('http://') or source.startswith('https://')):
                self.logger.info(f"Loading data from URL: {source}")
                return self.load_from_url(source, text_field=text_field)
            
            # File paths - detect type from extension
            elif isinstance(source, (str, Path)) and not source.lstrip().startswith('{') and not source.lstrip().startswith('['):
                file_path = str(source)
                if not detected_type:
                    detected_type, _ = mimetypes.guess_type(file_path)
                
                # Read file content based on type
                if detected_type and detected_type.startswith('text/'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                elif detected_type:
                    # Binary file
                    return self._process_file(file_path, detected_type, text_field)
                else:
                    # Try to detect from content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.lstrip().startswith('{') or content.lstrip().startswith('['):
                                detected_type = "application/json"
                            elif re.match(r'[\w,]+\n[\w,]+', content):
                                detected_type = "text/csv"
                            else:
                                detected_type = "text/plain"
                    except UnicodeDecodeError:
                        # Binary file
                        return self._process_file(file_path, "application/octet-stream", text_field)
            
            # Direct JSON strings
            elif isinstance(source, str) and (source.lstrip().startswith('{') or source.lstrip().startswith('[')):
                content = source
                detected_type = "application/json"
            
            # Direct dictionaries/lists
            elif isinstance(source, (dict, list)):
                return self._process_json(source, text_field)
            
            # File-like objects
            elif hasattr(source, 'read'):
                content = source.read()
                # Try to determine content type
                if not detected_type:
                    if isinstance(content, str):
                        if content.lstrip().startswith('{') or content.lstrip().startswith('['):
                            detected_type = "application/json"
                        elif re.match(r'[\w,]+\n[\w,]+', content):
                            detected_type = "text/csv"
                        else:
                            detected_type = "text/plain"
                    else:
                        # Binary content
                        return self._process_binary(content, "application/octet-stream", text_field)
            
            # Other string content
            elif isinstance(source, str):
                content = source
                if not detected_type:
                    if content.lstrip().startswith('{') or content.lstrip().startswith('['):
                        detected_type = "application/json"
                    elif re.match(r'[\w,]+\n[\w,]+', content):
                        detected_type = "text/csv"
                    else:
                        detected_type = "text/plain"
            
            # Process content based on detected type
            if not detected_type:
                detected_type = "text/plain"  # Default to text
                
            handler = self.content_type_handlers.get(detected_type, self._process_text)
            return handler(content, text_field)
            
        except Exception as e:
            self.logger.error(f"Error loading from source: {str(e)}")
            raise InputValidationError(f"Failed to load data from source: {str(e)}")
    
    def load_from_url(self, url: str, text_field: str = 'text') -> List[Dict]:
        """
        Load data from a URL with automatic content detection.
        
        Args:
            url: URL to load data from
            text_field: Field name for text content
            
        Returns:
            List of document dictionaries
        """
        try:
            # Send HTTP request
            headers = {
                'User-Agent': 'AI-Data-SDK/1.0 (https://example.com/ai-data-sdk)'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Get content type
            content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
            
            # Process based on content type
            if content_type == 'application/json':
                return self._process_json(response.text, text_field)
            elif content_type in ('text/csv', 'application/csv'):
                return self._process_csv(response.text, text_field)
            elif content_type == 'text/html':
                return self._process_html(response.text, text_field, url=url)
            elif content_type.startswith('text/'):
                return self._process_text(response.text, text_field)
            else:
                # Unknown content type, try to process as HTML
                if '<html' in response.text.lower() or '<body' in response.text.lower():
                    return self._process_html(response.text, text_field, url=url)
                else:
                    # Default to text
                    return self._process_text(response.text, text_field)
                    
        except Exception as e:
            self.logger.error(f"Error loading from URL {url}: {str(e)}")
            raise InputValidationError(f"Failed to load data from URL: {str(e)}")
    
    def load_from_directory(self, directory: Union[str, Path], 
                          pattern: str = "*",
                          recursive: bool = True,
                          text_field: str = 'text') -> List[Dict]:
        """
        Load data from all files in a directory.
        
        Args:
            directory: Directory path
            pattern: Glob pattern for matching files
            recursive: Whether to search subdirectories
            text_field: Field name for text content
            
        Returns:
            List of document dictionaries
        """
        try:
            # Ensure directory exists
            path = Path(directory)
            if not path.is_dir():
                raise InputValidationError(f"Directory not found: {directory}")
            
            # Find matching files
            if recursive:
                files = list(path.glob(f"**/{pattern}"))
            else:
                files = list(path.glob(pattern))
                
            if not files:
                self.logger.warning(f"No files found in {directory} matching pattern {pattern}")
                return []
                
            # Process files in parallel
            all_documents = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {
                    executor.submit(self.load_from_source, str(file), text_field=text_field): file
                    for file in files
                }
                
                for future in concurrent.futures.as_completed(future_to_file):
                    file = future_to_file[future]
                    try:
                        documents = future.result()
                        # Add file path metadata
                        for doc in documents:
                            doc['source_file'] = str(file)
                        all_documents.extend(documents)
                    except Exception as e:
                        self.logger.error(f"Error processing file {file}: {str(e)}")
                        
            return all_documents
            
        except Exception as e:
            self.logger.error(f"Error loading from directory {directory}: {str(e)}")
            raise InputValidationError(f"Failed to load data from directory: {str(e)}")
    
    def load_and_chunk(self, source: Union[str, Path, TextIO], 
                     chunk_size: int = 1000,
                     chunk_overlap: int = 200,
                     separator: str = "\n\n") -> List[Dict]:
        """
        Load text and split into overlapping chunks.
        
        Args:
            source: Source data (file path, URL, or string)
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks in characters
            separator: Preferred separator for chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        try:
            # Load full document
            documents = self.load_from_source(source)
            if not documents:
                return []
                
            # Extract text content
            if len(documents) == 1:
                # Single document, extract text
                doc = documents[0]
                text = next((doc[field] for field in doc if isinstance(doc[field], str) and len(doc[field]) > 100), "")
                metadata = {k: v for k, v in doc.items() if k != "text" and not (isinstance(v, str) and len(v) > 100)}
            else:
                # Multiple documents, concatenate texts
                texts = []
                metadata = {"document_count": len(documents)}
                for doc in documents:
                    text_fields = [field for field in doc if isinstance(doc[field], str) and len(doc[field]) > 50]
                    if text_fields:
                        texts.append(doc[text_fields[0]])
                text = separator.join(texts)
                
            # Split into chunks
            return self._split_text_into_chunks(text, chunk_size, chunk_overlap, separator, metadata)
            
        except Exception as e:
            self.logger.error(f"Error chunking content: {str(e)}")
            raise InputValidationError(f"Failed to chunk content: {str(e)}")
    
    def _split_text_into_chunks(self, text: str, chunk_size: int, chunk_overlap: int, 
                              separator: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """Split text into overlapping chunks."""
        if not text:
            return []
            
        chunks = []
        base_metadata = metadata or {}
        
        # If text is smaller than chunk size, return as is
        if len(text) <= chunk_size:
            processed_text = self._preprocess_text(text)
            return [{
                "text": processed_text,
                "chunk_index": 0,
                "chunk_count": 1,
                **base_metadata
            }]
            
        # Split by separator
        parts = text.split(separator)
        current_chunk = []
        current_size = 0
        chunk_index = 0
        
        for part in parts:
            part_size = len(part) + len(separator)
            
            # If adding this part would exceed chunk size and we have content
            if current_size + part_size > chunk_size and current_chunk:
                # Join current chunk and add to results
                chunk_text = separator.join(current_chunk)
                processed_text = self._preprocess_text(chunk_text)
                
                chunks.append({
                    "text": processed_text,
                    "chunk_index": chunk_index,
                    "chunk_size": len(processed_text),
                    **base_metadata
                })
                
                chunk_index += 1
                
                # Start new chunk with overlap by including the last few parts
                overlap_size = 0
                overlap_parts = []
                
                for prev_part in reversed(current_chunk):
                    prev_size = len(prev_part) + len(separator)
                    if overlap_size + prev_size <= chunk_overlap:
                        overlap_parts.insert(0, prev_part)
                        overlap_size += prev_size
                    else:
                        break
                
                current_chunk = overlap_parts + [part]
                current_size = overlap_size + part_size
            else:
                # Add part to current chunk
                current_chunk.append(part)
                current_size += part_size
                
        # Add the last chunk if not empty
        if current_chunk:
            chunk_text = separator.join(current_chunk)
            processed_text = self._preprocess_text(chunk_text)
            
            chunks.append({
                "text": processed_text,
                "chunk_index": chunk_index,
                "chunk_size": len(processed_text),
                **base_metadata
            })
            
        # Add total chunk count to all chunks
        for chunk in chunks:
            chunk["chunk_count"] = len(chunks)
            
        return chunks
    
    def _process_json(self, content: Union[str, Dict, List], text_field: str) -> List[Dict]:
        """Process JSON content."""
        # Parse if string
        if isinstance(content, str):
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                raise InputValidationError(f"Invalid JSON: {str(e)}")
        else:
            data = content
            
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
                
        # Validate and preprocess documents
        valid_documents = []
        for doc in documents:
            if not isinstance(doc, dict):
                self.logger.warning(f"Skipping non-dictionary document: {doc}")
                continue
                
            # Apply preprocessors to text fields
            processed_doc = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    processed_doc[key] = self._preprocess_text(value)
                else:
                    processed_doc[key] = value
                    
            valid_documents.append(processed_doc)
            
        self.logger.info(f"Processed {len(valid_documents)} documents from JSON")
        return valid_documents
    
    def _process_csv(self, content: str, text_field: Optional[str] = None) -> List[Dict]:
        """Process CSV content."""
        # Parse CSV
        documents = []
        try:
            # Handle both file and string input
            if isinstance(content, str):
                lines = content.splitlines()
                reader = csv.reader(lines)
                rows = list(reader)
            else:
                reader = csv.reader(content)
                rows = list(reader)
                
            if not rows:
                return []
                
            # Process header
            headers = rows[0]
            if not text_field:
                # Use first column as text field
                text_field_index = 0
            else:
                # Find text field in headers
                if text_field in headers:
                    text_field_index = headers.index(text_field)
                else:
                    text_field_index = 0
                    
            # Process data rows
            for row in rows[1:]:
                if len(row) < len(headers):
                    # Pad missing values
                    row.extend([''] * (len(headers) - len(row)))
                    
                # Create document
                doc = {}
                for i, value in enumerate(row):
                    if i < len(headers):
                        # Apply preprocessors to text fields
                        if isinstance(value, str):
                            doc[headers[i]] = self._preprocess_text(value)
                        else:
                            doc[headers[i]] = value
                            
                documents.append(doc)
                
            self.logger.info(f"Processed {len(documents)} documents from CSV")
            return documents
            
        except Exception as e:
            self.logger.error(f"Error processing CSV: {str(e)}")
            raise InputValidationError(f"Failed to process CSV: {str(e)}")
    
    def _process_text(self, content: str, text_field: str, split_pattern: Optional[str] = None) -> List[Dict]:
        """Process plain text content."""
        if not content:
            return []
            
        # Split text into documents if pattern provided
        documents = []
        if split_pattern:
            # Split by pattern
            parts = re.split(split_pattern, content)
            for i, part in enumerate(parts):
                if part.strip():  # Skip empty parts
                    # Apply preprocessors
                    processed_text = self._preprocess_text(part.strip())
                    documents.append({
                        'id': f'doc_{i}',
                        text_field: processed_text
                    })
        else:
            # Treat as single document
            processed_text = self._preprocess_text(content)
            documents.append({
                'id': 'doc_0',
                text_field: processed_text
            })
            
        self.logger.info(f"Processed {len(documents)} documents from text")
        return documents
    
    def _process_html(self, content: str, text_field: str, url: Optional[str] = None) -> List[Dict]:
        """Process HTML content using trafilatura."""
        try:
            # Extract text using trafilatura
            extracted_text = trafilatura.extract(content, include_links=True, include_images=True)
            
            if not extracted_text:
                self.logger.warning("No text content extracted from HTML")
                # Fallback to basic extraction
                text = re.sub(r'<[^>]+>', ' ', content)
                text = re.sub(r'\s+', ' ', text).strip()
                extracted_text = text
                
            # Create document
            processed_text = self._preprocess_text(extracted_text)
            document = {
                text_field: processed_text
            }
            
            # Add metadata if URL is provided
            if url:
                document['source_url'] = url
                document['title'] = self._extract_title(content) or url
                
            self.logger.info(f"Processed HTML content, extracted {len(processed_text)} characters")
            return [document]
            
        except Exception as e:
            self.logger.error(f"Error processing HTML: {str(e)}")
            raise InputValidationError(f"Failed to process HTML: {str(e)}")
    
    def _extract_title(self, html: str) -> Optional[str]:
        """Extract title from HTML content."""
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def _process_file(self, file_path: str, content_type: str, text_field: str) -> List[Dict]:
        """Process file based on content type."""
        # Handle different file types
        if content_type == "application/json":
            with open(file_path, 'r', encoding='utf-8') as f:
                return self._process_json(f.read(), text_field)
        elif content_type in ("text/csv", "application/csv"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return self._process_csv(f.read(), text_field)
        elif content_type.startswith("text/"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return self._process_text(f.read(), text_field)
        else:
            # Binary file - create metadata document
            file_info = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            document = {
                'id': self._generate_id(file_path),
                'filename': filename,
                'file_path': file_path,
                'content_type': content_type,
                'file_size': file_info.st_size,
                'last_modified': datetime.fromtimestamp(file_info.st_mtime).isoformat()
            }
            
            self.logger.info(f"Processed binary file: {filename}")
            return [document]
    
    def _process_binary(self, content: bytes, content_type: str, text_field: str) -> List[Dict]:
        """Process binary content."""
        # Create metadata document for binary content
        document = {
            'id': self._generate_id(content),
            'content_type': content_type,
            'content_size': len(content)
        }
        
        self.logger.info(f"Processed binary content: {len(content)} bytes")
        return [document]
    
    def _process_unsupported(self, content: Any, text_field: str) -> List[Dict]:
        """Process unsupported content type."""
        self.logger.warning(f"Unsupported content type")
        return []
    
    def _preprocess_text(self, text: str) -> str:
        """Apply preprocessing functions to text."""
        processed = text
        for preprocessor in self.preprocessors:
            processed = preprocessor(processed)
        return processed
    
    def _generate_id(self, content: Union[str, bytes]) -> str:
        """Generate a deterministic ID for content."""
        if isinstance(content, str):
            content_bytes = content.encode('utf-8')
        else:
            content_bytes = content
            
        return hashlib.md5(content_bytes).hexdigest()
    
    def add_preprocessor(self, preprocessor: Callable[[str], str]) -> None:
        """Add a preprocessor function to the processing pipeline."""
        self.preprocessors.append(preprocessor)
        
class WebCrawler:
    """
    Web crawler for extracting content from websites.
    """
    def __init__(self, 
                max_pages: int = 10,
                max_depth: int = 2,
                respect_robots: bool = True,
                follow_external: bool = False,
                delay: float = 0.5):
        """
        Initialize web crawler.
        
        Args:
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum crawl depth
            respect_robots: Whether to respect robots.txt
            follow_external: Whether to follow external links
            delay: Delay between requests in seconds
        """
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.respect_robots = respect_robots
        self.follow_external = follow_external
        self.delay = delay
        self.logger = logging.getLogger(__name__)
        
        # Initialize data ingester
        self.ingester = EnhancedDataIngester()
        
        # Initialize crawler state
        self.visited_urls = set()
        self.queue = []
        self.documents = []
        self.disallowed_patterns = []
    
    def crawl(self, start_url: str, text_field: str = 'text') -> List[Dict]:
        """
        Crawl a website starting from the provided URL.
        
        Args:
            start_url: Starting URL for crawl
            text_field: Field name for text content
            
        Returns:
            List of document dictionaries
        """
        # Reset state
        self.visited_urls = set()
        self.queue = [(start_url, 0)]  # (url, depth)
        self.documents = []
        
        # Parse domain
        domain = urllib.parse.urlparse(start_url).netloc
        self.base_url = f"{urllib.parse.urlparse(start_url).scheme}://{domain}"
        
        # Get robots.txt
        if self.respect_robots:
            self._process_robots_txt(self.base_url)
        
        # Process queue
        while self.queue and len(self.visited_urls) < self.max_pages:
            url, depth = self.queue.pop(0)
            
            # Check if already visited
            if url in self.visited_urls:
                continue
                
            # Check depth limit
            if depth > self.max_depth:
                continue
                
            # Check if allowed by robots.txt
            if self.respect_robots and self._is_disallowed(url):
                self.logger.info(f"Skipping disallowed URL: {url}")
                continue
                
            # Process URL
            try:
                self.logger.info(f"Crawling: {url}")
                
                # Add to visited
                self.visited_urls.add(url)
                
                # Fetch content
                headers = {
                    'User-Agent': 'AI-Data-SDK/1.0 (https://example.com/ai-data-sdk)'
                }
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Skip non-HTML content
                content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
                if content_type != 'text/html' and not content_type.startswith('text/'):
                    self.logger.info(f"Skipping non-HTML content: {content_type}")
                    continue
                
                # Extract text and add to documents
                documents = self.ingester._process_html(response.text, text_field, url=url)
                self.documents.extend(documents)
                
                # Extract links and add to queue
                if depth < self.max_depth:
                    links = self._extract_links(response.text, url)
                    for link in links:
                        # Check domain
                        link_domain = urllib.parse.urlparse(link).netloc
                        if not self.follow_external and link_domain != domain:
                            continue
                            
                        # Add to queue if not visited
                        if link not in self.visited_urls:
                            self.queue.append((link, depth + 1))
                
                # Respect delay
                import time
                time.sleep(self.delay)
                
            except Exception as e:
                self.logger.error(f"Error crawling {url}: {str(e)}")
                
        self.logger.info(f"Crawl complete: {len(self.visited_urls)} pages visited, {len(self.documents)} documents extracted")
        return self.documents
    
    def _process_robots_txt(self, base_url: str) -> None:
        """Process robots.txt and extract disallowed patterns."""
        try:
            # Fetch robots.txt
            robots_url = f"{base_url}/robots.txt"
            response = requests.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                # Extract disallowed patterns
                user_agent = "*"  # Default to all agents
                for line in lines:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                        
                    # Check User-Agent
                    if line.lower().startswith('user-agent:'):
                        user_agent = line.split(':', 1)[1].strip()
                        continue
                        
                    # Extract Disallow patterns
                    if line.lower().startswith('disallow:') and (user_agent == "*" or user_agent == "AI-Data-SDK"):
                        pattern = line.split(':', 1)[1].strip()
                        if pattern:
                            self.disallowed_patterns.append(pattern)
                            
                self.logger.info(f"Loaded {len(self.disallowed_patterns)} disallowed patterns from robots.txt")
            
        except Exception as e:
            self.logger.warning(f"Error processing robots.txt: {str(e)}")
    
    def _is_disallowed(self, url: str) -> bool:
        """Check if URL is disallowed by robots.txt."""
        path = urllib.parse.urlparse(url).path
        
        for pattern in self.disallowed_patterns:
            # Handle wildcards
            if pattern.endswith('*'):
                if path.startswith(pattern[:-1]):
                    return True
            elif path == pattern or path.startswith(pattern):
                return True
                
        return False
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML content."""
        links = []
        
        # Extract href attributes
        for match in re.finditer(r'<a\s+[^>]*href\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
            href = match.group(1).strip()
            
            # Skip fragment and javascript links
            if href.startswith('#') or href.startswith('javascript:'):
                continue
                
            # Resolve relative URLs
            if not href.startswith('http'):
                href = urllib.parse.urljoin(base_url, href)
                
            links.append(href)
            
        return links

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
    
def remove_duplicate_sentences(text: str) -> str:
    """Remove duplicate sentences from text."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    unique_sentences = []
    seen = set()
    
    for sentence in sentences:
        # Skip very short sentences
        if len(sentence) < 10:
            unique_sentences.append(sentence)
            continue
            
        # Normalize for comparison
        norm = re.sub(r'\s+', ' ', sentence.lower()).strip()
        if norm not in seen:
            seen.add(norm)
            unique_sentences.append(sentence)
            
    return ' '.join(unique_sentences)

# Convenience functions
def load_from_url(url: str, text_field: str = 'text') -> List[Dict]:
    """Load data from URL without instantiating a class."""
    ingester = EnhancedDataIngester()
    return ingester.load_from_url(url, text_field)

def load_and_chunk(source: Union[str, Path, TextIO], chunk_size: int = 1000) -> List[Dict]:
    """Load and chunk content without instantiating a class."""
    ingester = EnhancedDataIngester()
    return ingester.load_and_chunk(source, chunk_size)

def crawl_website(url: str, max_pages: int = 10) -> List[Dict]:
    """Crawl a website without instantiating a class."""
    crawler = WebCrawler(max_pages=max_pages)
    return crawler.crawl(url)