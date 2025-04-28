"""
Main client class for the AI Data SDK API
"""

import requests
import json
from typing import Dict, List, Optional, Union, Any
from .errors import APIError, AuthenticationError, InvalidRequestError, RateLimitError

class AIDataClient:
    """Client for interacting with the AI Data SDK API"""
    
    def __init__(self, api_key: str, base_url: str = None):
        """
        Initialize a client instance.
        
        Args:
            api_key: The API key to use for authentication
            base_url: The base URL of the API (optional)
        """
        self.api_key = api_key
        self.base_url = base_url or "https://zeedata.io"
        
    def _request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            data: Request data (for POST requests)
            
        Returns:
            API response as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            InvalidRequestError: If the request is invalid
            RateLimitError: If rate limits are exceeded
            APIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 200:
                return response.json()
            
            error_data = response.json() if response.content else {"error": "Unknown error"}
            
            if response.status_code == 401:
                raise AuthenticationError(error_data.get("error", "Authentication failed"))
            elif response.status_code == 400:
                raise InvalidRequestError(error_data.get("error", "Invalid request"), error_data.get("details"))
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            else:
                raise APIError(f"API error: {response.status_code}", error_data)
                
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request error: {str(e)}")
    
    # Embeddings API
    def create_embeddings(self, texts: List[str], model: str = "text-embedding-3-small", normalize: bool = True) -> Dict[str, Any]:
        """
        Generate embeddings for the provided texts.
        
        Args:
            texts: List of text strings to embed
            model: Embedding model to use
            normalize: Whether to normalize vectors
            
        Returns:
            Dictionary containing the embeddings and metadata
        """
        data = {
            "texts": texts,
            "model": model,
            "normalize": normalize
        }
        return self._request("POST", "/api/v1/embeddings", data)
    
    # Search API
    def search(self, 
               query_text: Optional[str] = None,
               query_vector: Optional[List[float]] = None,
               top_k: int = 10,
               filters: Optional[Dict[str, Any]] = None,
               hybrid_search_text: Optional[str] = None,
               hybrid_alpha: Optional[float] = None) -> Dict[str, Any]:
        """
        Search for similar documents using text or vector query.
        
        Args:
            query_text: Text to search for (required if query_vector not provided)
            query_vector: Vector to search with (required if query_text not provided)
            top_k: Number of results to return
            filters: Metadata filters to apply
            hybrid_search_text: Text for hybrid search
            hybrid_alpha: Weight for hybrid search (0 = vector only, 1 = text only)
            
        Returns:
            Search results with document matches
        """
        if not query_text and not query_vector:
            raise ValueError("Either query_text or query_vector must be provided")
            
        data = {
            "top_k": top_k
        }
        
        if query_text:
            data["query_text"] = query_text
        if query_vector:
            data["query_vector"] = query_vector
        if filters:
            data["filters"] = filters
        if hybrid_search_text:
            data["hybrid_search_text"] = hybrid_search_text
        if hybrid_alpha is not None:
            data["hybrid_alpha"] = hybrid_alpha
            
        return self._request("POST", "/api/v1/search", data)
    
    # PII Detection API
    def detect_pii(self, 
                  text: str,
                  pii_types: List[str] = None,
                  mask: bool = False,
                  mask_type: str = "type",
                  preserve_length: bool = False,
                  check_confidence: bool = False,
                  advanced_anonymize: bool = False,
                  consistent_replacements: bool = True) -> Dict[str, Any]:
        """
        Detect and optionally mask PII in text.
        
        Args:
            text: Text to analyze for PII
            pii_types: Types of PII to detect (default: ["all"])
            mask: Whether to apply masking
            mask_type: Type of masking: "type", "redact", "partial", "generic"
            preserve_length: Whether to preserve the length of masked strings
            check_confidence: Whether to include confidence scores
            advanced_anonymize: Use advanced anonymization instead of masking
            consistent_replacements: Replace same PII with same fake value
            
        Returns:
            PII detection results including processed text
        """
        data = {
            "text": text,
            "mask": mask,
            "mask_type": mask_type,
            "preserve_length": preserve_length,
            "check_confidence": check_confidence,
            "advanced_anonymize": advanced_anonymize,
            "consistent_replacements": consistent_replacements
        }
        
        if pii_types:
            data["pii_types"] = pii_types
            
        return self._request("POST", "/api/v1/pii", data)
    
    # Feedback API
    def submit_feedback(self, 
                       query_id: str,
                       result_id: str,
                       rating: int,
                       comments: str = None) -> Dict[str, Any]:
        """
        Submit feedback for search results.
        
        Args:
            query_id: ID of the query
            result_id: ID of the result being rated
            rating: Rating (1-5, where 5 is best)
            comments: Optional comments about the rating
            
        Returns:
            Confirmation of feedback submission
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        data = {
            "query_id": query_id,
            "result_id": result_id,
            "rating": rating
        }
        
        if comments:
            data["comments"] = comments
            
        return self._request("POST", "/api/v1/feedback", data)
    
    # IP Allowlist API (admin only)
    def get_ip_allowlist(self) -> Dict[str, Any]:
        """
        Get IP allowlist (admin only).
        
        Returns:
            List of allowed IP addresses
        """
        return self._request("GET", "/api/v1/ip-allowlist")
    
    def add_ip_to_allowlist(self, ip_address: str, description: str = None) -> Dict[str, Any]:
        """
        Add IP address to allowlist (admin only).
        
        Args:
            ip_address: IP address to add
            description: Optional description
            
        Returns:
            Confirmation of IP addition
        """
        data = {
            "ip_address": ip_address
        }
        
        if description:
            data["description"] = description
            
        return self._request("POST", "/api/v1/ip-allowlist", data)
    
    def remove_ip_from_allowlist(self, ip_address: str) -> Dict[str, Any]:
        """
        Remove IP address from allowlist (admin only).
        
        Args:
            ip_address: IP address to remove
            
        Returns:
            Confirmation of IP removal
        """
        return self._request("DELETE", "/api/v1/ip-allowlist", {"ip_address": ip_address})
    
    # Authentication - JWT token
    def generate_token(self, user_id: str) -> Dict[str, Any]:
        """
        Generate a JWT token for authentication.
        
        Args:
            user_id: User ID to include in the token
            
        Returns:
            Dict containing the JWT token
        """
        data = {
            "user_id": user_id,
            "api_key": self.api_key
        }
        
        return self._request("POST", "/api/v1/token", data)
