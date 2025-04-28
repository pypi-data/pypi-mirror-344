"""
Enhanced Data Quality Module

This module provides advanced tools for data validation, quality assessment, 
and schema enforcement.
"""

import logging
import re
import json
import statistics
from typing import List, Dict, Any, Optional, Union, Callable, Set, Tuple
import jsonschema
from datetime import datetime

from .validation import InputValidationError

# Set up logging
logger = logging.getLogger(__name__)

class DataQualityValidator:
    """
    Enhanced class for validating data quality and enforcing schemas.
    """
    def __init__(self, schema: Optional[Dict] = None, 
                max_errors: int = 100,
                enforce_schema: bool = True):
        """
        Initialize data quality validator.
        
        Args:
            schema: JSON Schema for validation
            max_errors: Maximum number of errors to collect
            enforce_schema: Whether to enforce schema validation
        """
        self.schema = schema
        self.max_errors = max_errors
        self.enforce_schema = enforce_schema
        self.logger = logger
        
        # Initialize validator if schema is provided
        self.validator = None
        if schema:
            self.validator = jsonschema.Draft7Validator(schema)
    
    def validate_document(self, document: Dict) -> Tuple[bool, List[Dict]]:
        """
        Validate a single document against schema and quality rules.
        
        Args:
            document: Document to validate
            
        Returns:
            Tuple of (is_valid, error_list)
        """
        errors = []
        
        # Schema validation
        if self.enforce_schema and self.validator:
            schema_errors = list(self.validator.iter_errors(document))
            for error in schema_errors[:self.max_errors]:
                errors.append({
                    "error_type": "schema_error",
                    "message": error.message,
                    "path": list(error.path) if error.path else [],
                    "schema_path": list(error.schema_path) if error.schema_path else []
                })
            
            # If schema validation failed, return immediately
            if errors:
                return False, errors
        
        # Quality validation
        quality_errors = self._validate_quality(document)
        errors.extend(quality_errors)
        
        return len(errors) == 0, errors
    
    def _validate_quality(self, document: Dict) -> List[Dict]:
        """Perform quality validation on a document."""
        errors = []
        
        # Check for empty values in required fields
        if self.schema and 'required' in self.schema and 'properties' in self.schema:
            for field in self.schema['required']:
                if field in document:
                    value = document[field]
                    field_props = self.schema['properties'].get(field, {})
                    
                    # Check for empty strings
                    if field_props.get('type') == 'string' and isinstance(value, str) and not value.strip():
                        errors.append({
                            "error_type": "quality_error",
                            "field": field,
                            "message": f"Field '{field}' is empty"
                        })
                        
                    # Check for too short text
                    if field_props.get('type') == 'string' and isinstance(value, str) and len(value.strip()) < 3:
                        errors.append({
                            "error_type": "quality_warning",
                            "field": field,
                            "message": f"Field '{field}' is very short ({len(value.strip())} chars)"
                        })
                        
                    # Check for very large arrays
                    if field_props.get('type') == 'array' and isinstance(value, list) and len(value) > 1000:
                        errors.append({
                            "error_type": "quality_warning",
                            "field": field,
                            "message": f"Field '{field}' has a very large array ({len(value)} items)"
                        })
        
        # Generic quality checks for all documents
        
        # Check for duplicate values in arrays
        for field, value in document.items():
            if isinstance(value, list):
                if len(value) != len(set(str(x) for x in value)):
                    errors.append({
                        "error_type": "quality_warning",
                        "field": field,
                        "message": f"Field '{field}' contains duplicate values"
                    })
        
        # Check for HTML content in text fields
        for field, value in document.items():
            if isinstance(value, str) and len(value) > 10:
                if re.search(r'<\/?[a-z][\s\S]*>', value):
                    errors.append({
                        "error_type": "quality_warning",
                        "field": field,
                        "message": f"Field '{field}' appears to contain HTML markup"
                    })
        
        return errors
    
    def validate_dataset(self, documents: List[Dict]) -> Dict:
        """
        Validate a dataset of documents.
        
        Args:
            documents: List of documents to validate
            
        Returns:
            Validation results with statistics
        """
        if not documents:
            return {
                "valid": True,
                "document_count": 0,
                "error_count": 0,
                "error_documents": [],
                "stats": {}
            }
        
        # Validate each document
        valid_count = 0
        error_count = 0
        error_documents = []
        all_errors = []
        
        for i, doc in enumerate(documents):
            is_valid, errors = self.validate_document(doc)
            
            if is_valid:
                valid_count += 1
            else:
                error_count += 1
                error_documents.append({
                    "document_index": i,
                    "errors": errors
                })
                all_errors.extend(errors)
        
        # Calculate statistics
        field_presence = {}
        field_value_counts = {}
        field_stats = {}
        
        # Analyze all fields
        for doc in documents:
            for field, value in doc.items():
                # Track field presence
                if field not in field_presence:
                    field_presence[field] = 0
                field_presence[field] += 1
                
                # Track value distributions for categorical fields
                if isinstance(value, (str, int, bool)) or value is None:
                    if field not in field_value_counts:
                        field_value_counts[field] = {}
                    
                    value_str = str(value)
                    if value_str not in field_value_counts[field]:
                        field_value_counts[field][value_str] = 0
                    field_value_counts[field][value_str] += 1
                
                # Calculate statistics for numeric fields
                if isinstance(value, (int, float)) and field not in field_stats:
                    numeric_values = [doc.get(field) for doc in documents 
                                     if isinstance(doc.get(field), (int, float))]
                    
                    if numeric_values:
                        field_stats[field] = {
                            "min": min(numeric_values),
                            "max": max(numeric_values),
                            "mean": sum(numeric_values) / len(numeric_values),
                            "median": statistics.median(numeric_values) if len(numeric_values) > 0 else None
                        }
        
        # Calculate proportions
        field_presence_pct = {field: count / len(documents) * 100 
                             for field, count in field_presence.items()}
        
        # Identify potential schema issues
        schema_insights = []
        
        # Check for inconsistent field presence
        for field, pct in field_presence_pct.items():
            if 5 < pct < 95:
                schema_insights.append({
                    "type": "inconsistent_field",
                    "field": field,
                    "message": f"Field '{field}' appears in {pct:.1f}% of documents"
                })
        
        # Check for inconsistent field types
        for field in field_presence:
            field_types = set()
            for doc in documents:
                if field in doc:
                    field_types.add(type(doc[field]).__name__)
            
            if len(field_types) > 1:
                schema_insights.append({
                    "type": "inconsistent_type",
                    "field": field,
                    "message": f"Field '{field}' has multiple types: {', '.join(field_types)}"
                })
        
        # Suggest data type enforcement for fields with consistent types
        field_type_suggestions = {}
        for field in field_presence:
            field_types = [type(doc[field]).__name__ for doc in documents if field in doc]
            if len(set(field_types)) == 1 and len(field_types) > len(documents) / 2:
                field_type_suggestions[field] = field_types[0]
        
        return {
            "valid": error_count == 0,
            "document_count": len(documents),
            "valid_count": valid_count,
            "error_count": error_count,
            "error_documents": error_documents,
            "field_presence": field_presence,
            "field_presence_pct": field_presence_pct,
            "value_distributions": field_value_counts,
            "numeric_stats": field_stats,
            "schema_insights": schema_insights,
            "type_suggestions": field_type_suggestions
        }
    
    def generate_schema(self, documents: List[Dict], 
                      threshold: float = 0.8,
                      include_examples: bool = True) -> Dict:
        """
        Generate a JSON schema from a dataset of documents.
        
        Args:
            documents: List of documents to analyze
            threshold: Proportion threshold for required fields (0.0-1.0)
            include_examples: Whether to include example values in schema
            
        Returns:
            Generated JSON schema
        """
        if not documents:
            return {"type": "object", "properties": {}}
        
        # Collect all field names and types
        fields = {}
        examples = {}
        
        for doc in documents:
            for field, value in doc.items():
                # Track field types
                field_type = self._get_json_schema_type(value)
                
                if field not in fields:
                    fields[field] = {"types": set(), "count": 0}
                    examples[field] = []
                
                fields[field]["types"].add(field_type)
                fields[field]["count"] += 1
                
                # Track examples (up to 3 per field)
                if include_examples and len(examples[field]) < 3 and value is not None:
                    if field_type == "string" and isinstance(value, str):
                        # Truncate long strings
                        example_value = value[:100] + "..." if len(value) > 100 else value
                    else:
                        example_value = value
                        
                    if example_value not in examples[field]:
                        examples[field].append(example_value)
        
        # Generate schema
        properties = {}
        required = []
        
        for field, info in fields.items():
            types = info["types"]
            count = info["count"]
            proportion = count / len(documents)
            
            # Determine field schema
            if len(types) == 1:
                # Single type
                field_type = next(iter(types))
                properties[field] = {"type": field_type}
                
                # Add formats for common string patterns
                if field_type == "string" and include_examples and examples[field]:
                    format_type = self._detect_string_format(examples[field])
                    if format_type:
                        properties[field]["format"] = format_type
            else:
                # Multiple types
                field_types = list(types)
                properties[field] = {"type": field_types}
            
            # Add examples if requested
            if include_examples and examples[field]:
                properties[field]["examples"] = examples[field]
                
            # Add field to required list if it appears in enough documents
            if proportion >= threshold:
                required.append(field)
        
        # Create schema
        schema = {
            "type": "object",
            "properties": properties,
            "required": required
        }
        
        return schema
    
    def _get_json_schema_type(self, value: Any) -> str:
        """Determine the JSON Schema type for a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"  # Default to string for unknown types
    
    def _detect_string_format(self, examples: List[str]) -> Optional[str]:
        """Detect common string formats from examples."""
        # Try to detect common formats from the examples
        if not examples:
            return None
            
        example = examples[0] if isinstance(examples[0], str) else str(examples[0])
        
        # Check for date-time format
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', example):
            return "date-time"
            
        # Check for date format
        if re.match(r'^\d{4}-\d{2}-\d{2}$', example):
            return "date"
            
        # Check for email format
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', example):
            return "email"
            
        # Check for URI format
        if re.match(r'^https?://', example):
            return "uri"
            
        # Check for UUID format
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', example.lower()):
            return "uuid"
            
        return None
    
    def set_schema(self, schema: Dict) -> None:
        """Set the schema for validation."""
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema)
    
    def calculate_quality_score(self, document: Dict) -> float:
        """
        Calculate a quality score for a document (0.0-1.0).
        
        Args:
            document: Document to evaluate
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        # Basic validity check
        is_valid, errors = self.validate_document(document)
        if not is_valid:
            # Calculate penalty based on number and severity of errors
            error_penalty = min(1.0, len(errors) * 0.1)
            return max(0.0, 0.5 - error_penalty)
        
        # Start with a perfect score
        score = 1.0
        penalties = []
        
        # Check text field quality for specific fields
        if self.schema and 'properties' in self.schema:
            for field, props in self.schema['properties'].items():
                if field in document and props.get('type') == 'string':
                    value = document[field]
                    if isinstance(value, str):
                        # Penalize very short text
                        if len(value.strip()) < 5:
                            penalties.append(0.05)
                        
                        # Penalize text with weird character distributions
                        letter_ratio = sum(c.isalpha() for c in value) / max(1, len(value))
                        if letter_ratio < 0.5:
                            penalties.append(0.1)
                        
                        # Penalize repetitive text
                        if len(value) > 20 and len(set(value.lower())) / len(value) < 0.3:
                            penalties.append(0.15)
        
        # Apply penalties
        total_penalty = min(0.9, sum(penalties))
        score -= total_penalty
        
        return max(0.1, score)

class DatasetAnalyzer:
    """
    Analyzer for datasets to identify patterns, anomalies, and quality issues.
    """
    def __init__(self, text_field: str = "text"):
        """
        Initialize dataset analyzer.
        
        Args:
            text_field: Default field name containing text content
        """
        self.text_field = text_field
        self.logger = logger
    
    def analyze_dataset(self, documents: List[Dict], text_field: Optional[str] = None) -> Dict:
        """
        Analyze a dataset of documents.
        
        Args:
            documents: List of documents to analyze
            text_field: Field name containing text content (overrides default)
            
        Returns:
            Analysis results with statistics and insights
        """
        if not documents:
            return {
                "document_count": 0,
                "insights": [],
                "stats": {}
            }
        
        field = text_field or self.text_field
        
        # Calculate basic statistics
        document_count = len(documents)
        field_stats = self._calculate_field_stats(documents)
        text_stats = self._analyze_text_fields(documents, field)
        
        # Generate insights
        insights = []
        
        # Identify highly correlated fields
        correlations = self._identify_correlations(documents)
        for corr in correlations:
            if corr["correlation"] > 0.9:
                insights.append({
                    "type": "high_correlation",
                    "fields": [corr["field1"], corr["field2"]],
                    "message": f"Fields '{corr['field1']}' and '{corr['field2']}' are highly correlated ({corr['correlation']:.2f})"
                })
        
        # Identify potential data quality issues
        for f, stats in field_stats.items():
            # Check for high missing value rates
            if stats.get("missing_rate", 0) > 0.3:
                insights.append({
                    "type": "high_missing_rate",
                    "field": f,
                    "message": f"Field '{f}' has a high missing value rate ({stats['missing_rate']:.2f})"
                })
            
            # Check for high cardinality
            if stats.get("type") == "categorical" and stats.get("cardinality", 0) > 100:
                insights.append({
                    "type": "high_cardinality",
                    "field": f,
                    "message": f"Field '{f}' has unusually high cardinality ({stats['cardinality']})"
                })
        
        # Identify outliers in numeric fields
        numeric_outliers = self._detect_numeric_outliers(documents)
        for outlier in numeric_outliers:
            insights.append({
                "type": "numeric_outlier",
                "field": outlier["field"],
                "message": f"Found {outlier['count']} outliers in field '{outlier['field']}'"
            })
        
        return {
            "document_count": document_count,
            "field_stats": field_stats,
            "text_stats": text_stats,
            "correlations": correlations,
            "outliers": numeric_outliers,
            "insights": insights
        }
    
    def _calculate_field_stats(self, documents: List[Dict]) -> Dict:
        """Calculate statistics for all fields in the documents."""
        # Track field presence and types
        field_presence = {}
        field_types = {}
        
        for doc in documents:
            for field, value in doc.items():
                # Track field presence
                if field not in field_presence:
                    field_presence[field] = 0
                field_presence[field] += 1
                
                # Track field types
                value_type = type(value).__name__
                if field not in field_types:
                    field_types[field] = {}
                if value_type not in field_types[field]:
                    field_types[field][value_type] = 0
                field_types[field][value_type] += 1
        
        # Calculate statistics for each field
        results = {}
        for field in field_presence:
            presence_count = field_presence[field]
            missing_rate = 1 - (presence_count / len(documents))
            
            # Determine field type (dominant type)
            dominant_type = max(field_types[field].items(), key=lambda x: x[1])[0]
            
            field_stats = {
                "presence_count": presence_count,
                "missing_rate": missing_rate,
                "types": field_types[field],
                "type": dominant_type
            }
            
            # Calculate additional statistics based on field type
            if dominant_type in ("int", "float"):
                # Numeric field
                values = [doc[field] for doc in documents if field in doc and isinstance(doc[field], (int, float))]
                if values:
                    field_stats.update({
                        "min": min(values),
                        "max": max(values),
                        "mean": sum(values) / len(values),
                        "median": statistics.median(values) if len(values) > 0 else None,
                        "std_dev": statistics.stdev(values) if len(values) > 1 else 0
                    })
            elif dominant_type == "str":
                # String field
                values = [doc[field] for doc in documents if field in doc and isinstance(doc[field], str)]
                if values:
                    lengths = [len(v) for v in values]
                    field_stats.update({
                        "min_length": min(lengths),
                        "max_length": max(lengths),
                        "avg_length": sum(lengths) / len(lengths),
                        "cardinality": len(set(values))
                    })
                    
                    # Check if field is categorical (low cardinality)
                    if len(set(values)) < min(20, len(values) / 5):
                        field_stats["categorical"] = True
                        
                        # Calculate value distribution
                        value_counts = {}
                        for v in values:
                            if v not in value_counts:
                                value_counts[v] = 0
                            value_counts[v] += 1
                            
                        field_stats["value_distribution"] = {
                            k: v / len(values) for k, v in sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                        }
            
            results[field] = field_stats
        
        return results
    
    def _analyze_text_fields(self, documents: List[Dict], text_field: str) -> Dict:
        """Analyze text fields for content statistics."""
        # Collect all text content
        texts = [doc[text_field] for doc in documents if text_field in doc and isinstance(doc[text_field], str)]
        
        if not texts:
            return {}
        
        # Calculate text statistics
        word_counts = [len(re.findall(r'\b\w+\b', text)) for text in texts]
        
        return {
            "count": len(texts),
            "min_words": min(word_counts) if word_counts else 0,
            "max_words": max(word_counts) if word_counts else 0,
            "avg_words": sum(word_counts) / len(word_counts) if word_counts else 0,
            "total_words": sum(word_counts),
            "vocabulary_size": len(set(re.findall(r'\b\w+\b', ' '.join(texts).lower())))
        }
    
    def _identify_correlations(self, documents: List[Dict]) -> List[Dict]:
        """Identify correlations between fields."""
        # Identify numeric fields
        numeric_fields = []
        for field in documents[0].keys() if documents else []:
            if all(isinstance(doc.get(field), (int, float)) for doc in documents if field in doc):
                numeric_fields.append(field)
        
        if len(numeric_fields) < 2:
            return []
        
        # Calculate correlations
        correlations = []
        for i, field1 in enumerate(numeric_fields):
            for field2 in numeric_fields[i+1:]:
                # Get paired values
                pairs = [
                    (doc.get(field1), doc.get(field2))
                    for doc in documents
                    if field1 in doc and field2 in doc and
                    isinstance(doc[field1], (int, float)) and
                    isinstance(doc[field2], (int, float))
                ]
                
                if len(pairs) < 10:
                    continue
                    
                # Calculate correlation coefficient
                x_values, y_values = zip(*pairs)
                
                try:
                    correlation = self._calculate_correlation(x_values, y_values)
                    correlations.append({
                        "field1": field1,
                        "field2": field2,
                        "correlation": correlation,
                        "sample_size": len(pairs)
                    })
                except:
                    # Skip if correlation calculation fails
                    pass
        
        return correlations
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        n = len(x)
        if n != len(y) or n == 0:
            return 0
            
        # Calculate means
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        # Calculate covariance and standard deviations
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = (sum((val - mean_x) ** 2 for val in x)) ** 0.5
        std_dev_y = (sum((val - mean_y) ** 2 for val in y)) ** 0.5
        
        # Avoid division by zero
        if std_dev_x == 0 or std_dev_y == 0:
            return 0
            
        return covariance / (std_dev_x * std_dev_y)
    
    def _detect_numeric_outliers(self, documents: List[Dict]) -> List[Dict]:
        """Detect outliers in numeric fields using Z-score."""
        outliers = []
        
        # Identify numeric fields
        for field in documents[0].keys() if documents else []:
            values = [doc[field] for doc in documents if field in doc and isinstance(doc[field], (int, float))]
            
            if len(values) < 10:
                continue
                
            # Calculate mean and standard deviation
            mean = sum(values) / len(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0
            
            if std_dev == 0:
                continue
                
            # Identify outliers (Z-score > 3)
            outlier_values = [val for val in values if abs(val - mean) / std_dev > 3]
            
            if outlier_values:
                outliers.append({
                    "field": field,
                    "count": len(outlier_values),
                    "mean": mean,
                    "std_dev": std_dev,
                    "min_outlier": min(outlier_values),
                    "max_outlier": max(outlier_values)
                })
        
        return outliers

# Helper functions
def validate_document(document: Dict, schema: Optional[Dict] = None) -> Tuple[bool, List[Dict]]:
    """Validate a single document without instantiating a class."""
    validator = DataQualityValidator(schema=schema)
    return validator.validate_document(document)

def analyze_dataset(documents: List[Dict], text_field: str = "text") -> Dict:
    """Analyze a dataset without instantiating a class."""
    analyzer = DatasetAnalyzer(text_field=text_field)
    return analyzer.analyze_dataset(documents, text_field)

def generate_schema(documents: List[Dict], threshold: float = 0.8) -> Dict:
    """Generate a JSON schema from documents without instantiating a class."""
    validator = DataQualityValidator()
    return validator.generate_schema(documents, threshold)