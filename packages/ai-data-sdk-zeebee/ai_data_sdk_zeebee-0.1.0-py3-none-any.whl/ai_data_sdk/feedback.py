"""
Drift & Feedback Module

This module provides tools for collecting user feedback and detecting embedding drift.
"""

import logging
import datetime
from typing import Dict, List, Any, Optional, Union
import numpy as np

class FeedbackCollector:
    """
    Class for collecting user feedback and detecting embedding drift.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.feedback_store = []
        self.historical_embeddings = {}
    
    def add_user_feedback(self, query_id: str, result_id: str, 
                        rating: int, comments: Optional[str] = None,
                        user_id: Optional[str] = None) -> Dict:
        """
        Add user feedback for a search result.
        
        Args:
            query_id: ID of the query
            result_id: ID of the result being rated
            rating: Rating (1-5)
            comments: Optional comments
            user_id: Optional user ID
            
        Returns:
            Dictionary with feedback details and ID
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
            
        feedback = {
            "feedback_id": f"fb_{len(self.feedback_store)}",
            "timestamp": datetime.datetime.now().isoformat(),
            "query_id": query_id,
            "result_id": result_id,
            "rating": rating,
            "comments": comments,
            "user_id": user_id
        }
        
        self.feedback_store.append(feedback)
        self.logger.debug(f"Added user feedback: {feedback['feedback_id']}")
        
        return feedback
    
    def get_feedback_stats(self, query_id: Optional[str] = None, 
                         result_id: Optional[str] = None,
                         user_id: Optional[str] = None) -> Dict:
        """
        Get statistics about collected feedback.
        
        Args:
            query_id: Optional filter by query ID
            result_id: Optional filter by result ID
            user_id: Optional filter by user ID
            
        Returns:
            Dictionary with feedback statistics
        """
        filtered_feedback = self.feedback_store
        
        # Apply filters
        if query_id:
            filtered_feedback = [fb for fb in filtered_feedback if fb["query_id"] == query_id]
            
        if result_id:
            filtered_feedback = [fb for fb in filtered_feedback if fb["result_id"] == result_id]
            
        if user_id:
            filtered_feedback = [fb for fb in filtered_feedback if fb["user_id"] == user_id]
            
        # Calculate statistics
        if not filtered_feedback:
            return {
                "count": 0,
                "average_rating": None,
                "rating_distribution": {
                    "1": 0, "2": 0, "3": 0, "4": 0, "5": 0
                }
            }
            
        # Calculate average rating
        ratings = [fb["rating"] for fb in filtered_feedback]
        avg_rating = sum(ratings) / len(ratings)
        
        # Calculate rating distribution
        distribution = {
            "1": ratings.count(1),
            "2": ratings.count(2),
            "3": ratings.count(3),
            "4": ratings.count(4),
            "5": ratings.count(5)
        }
        
        return {
            "count": len(filtered_feedback),
            "average_rating": avg_rating,
            "rating_distribution": distribution
        }
    
    def register_embedding_snapshot(self, domain: str, embeddings: List[List[float]]) -> None:
        """
        Register a snapshot of embeddings for drift detection.
        
        Args:
            domain: Domain identifier for this embedding set
            embeddings: List of embedding vectors
        """
        if not embeddings:
            return
            
        timestamp = datetime.datetime.now().isoformat()
        
        # Calculate statistics for the embedding set
        np_embeddings = np.array(embeddings)
        
        stats = {
            "timestamp": timestamp,
            "count": len(embeddings),
            "mean": np_embeddings.mean(axis=0).tolist(),
            "std": np_embeddings.std(axis=0).tolist(),
            "min": np_embeddings.min(axis=0).tolist(),
            "max": np_embeddings.max(axis=0).tolist()
        }
        
        # Initialize domain if not exists
        if domain not in self.historical_embeddings:
            self.historical_embeddings[domain] = []
            
        # Add statistics
        self.historical_embeddings[domain].append(stats)
        self.logger.debug(f"Registered embedding snapshot for domain: {domain}")
    
    def detect_drift(self, domain: str, current_embeddings: List[List[float]], 
                   threshold: float = 0.1) -> Dict:
        """
        Detect drift in embeddings compared to historical snapshots.
        
        Args:
            domain: Domain identifier
            current_embeddings: Current embedding vectors
            threshold: Threshold for significant drift
            
        Returns:
            Dictionary with drift detection results
        """
        if domain not in self.historical_embeddings or not self.historical_embeddings[domain]:
            return {
                "has_historical_data": False,
                "drift_detected": False,
                "message": "No historical data available for comparison"
            }
            
        if not current_embeddings:
            return {
                "has_historical_data": True,
                "drift_detected": False,
                "message": "No current embeddings provided for comparison"
            }
            
        # Get most recent historical snapshot
        latest_snapshot = self.historical_embeddings[domain][-1]
        
        # Calculate statistics for current embeddings
        np_embeddings = np.array(current_embeddings)
        current_mean = np_embeddings.mean(axis=0)
        
        # Calculate mean difference
        historical_mean = np.array(latest_snapshot["mean"])
        mean_diff = np.abs(current_mean - historical_mean).mean()
        
        # Detect drift
        drift_detected = mean_diff > threshold
        
        return {
            "has_historical_data": True,
            "drift_detected": drift_detected,
            "drift_score": float(mean_diff),
            "threshold": threshold,
            "historical_snapshot_time": latest_snapshot["timestamp"],
            "message": f"Drift {'detected' if drift_detected else 'not detected'} (score: {mean_diff:.4f}, threshold: {threshold})"
        }

# Helper functions
def add_user_feedback(query_id: str, result_id: str, rating: int, 
                     comments: Optional[str] = None, user_id: Optional[str] = None) -> Dict:
    """Add user feedback without instantiating a class"""
    collector = FeedbackCollector()
    return collector.add_user_feedback(query_id, result_id, rating, comments, user_id)

def detect_drift(domain: str, historical_embeddings: List[List[float]], 
                current_embeddings: List[List[float]], threshold: float = 0.1) -> Dict:
    """Simplified drift detection helper"""
    collector = FeedbackCollector()
    collector.register_embedding_snapshot(domain, historical_embeddings)
    return collector.detect_drift(domain, current_embeddings, threshold)
