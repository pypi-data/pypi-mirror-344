"""
Enhanced Configuration Module

This module provides a robust configuration system for the AI Data SDK, supporting
environment variables, configuration files, and validation.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Configuration error exception."""
    pass

class EnhancedConfig:
    """
    Enhanced configuration management class with validation.
    """
    # Default configuration
    DEFAULT_CONFIG = {
        # API Settings
        "api": {
            "host": "0.0.0.0",
            "port": 5000,
            "debug": False,
            "workers": 1,
            "timeout": 60
        },
        
        # Database Settings
        "database": {
            "uri": None,  # Will use environment variable if None
            "pool_size": 5,
            "pool_recycle": 300,
            "pool_pre_ping": True
        },
        
        # Embedding Settings
        "embedding": {
            "model": "text-embedding-3-small",
            "dimension": 1536,
            "batch_size": 100,
            "normalize_vectors": True
        },
        
        # Vector DB Settings
        "vector_db": {
            "distance_metric": "cosine",
            "index_type": "memory",
            "cache_size": 1000
        },
        
        # PII Detection Settings
        "pii": {
            "enabled": True,
            "confidence_threshold": 0.5,
            "default_mask_type": "type"
        },
        
        # Quality Settings
        "quality": {
            "validation_enabled": True,
            "schema_threshold": 0.8,
            "max_errors": 100
        },
        
        # Ingestion Settings
        "ingestion": {
            "max_workers": 4,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "respect_robots_txt": True
        },
        
        # Logging Settings
        "logging": {
            "level": "INFO",
            "file": None,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
    
    # Required environment variables
    REQUIRED_ENV_VARS = [
        "OPENAI_API_KEY"  # OpenAI API key is required
    ]
    
    # Optional environment variables with default values
    OPTIONAL_ENV_VARS = {
        "DATABASE_URL": None,
        "LOG_LEVEL": "INFO",
        "API_HOST": "0.0.0.0",
        "API_PORT": "5000",
        "DEBUG": "False"
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Optional path to configuration file
        """
        # Load default config
        self.config = self.DEFAULT_CONFIG.copy()
        
        # Load from file if provided
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
            
        # Override with environment variables
        self._load_from_env()
        
        # Validate configuration
        self._validate_config()
        
        # Configure logging
        self._configure_logging()
        
    def _load_from_file(self, config_path: str) -> None:
        """Load configuration from file."""
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                
            # Merge with default config (deep merge)
            self._deep_merge(self.config, file_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.warning(f"Error loading configuration from {config_path}: {str(e)}")
            
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Load required environment variables
        for var in self.REQUIRED_ENV_VARS:
            if var in os.environ:
                # Store in separate dict to avoid exposing secrets in config
                if var == "OPENAI_API_KEY":
                    self.openai_api_key = os.environ[var]
            else:
                logger.warning(f"Required environment variable {var} not set")
                
        # Load optional environment variables
        for var, default in self.OPTIONAL_ENV_VARS.items():
            value = os.environ.get(var, default)
            
            if var == "DATABASE_URL" and value:
                self.config["database"]["uri"] = value
            elif var == "LOG_LEVEL" and value:
                self.config["logging"]["level"] = value
            elif var == "API_HOST" and value:
                self.config["api"]["host"] = value
            elif var == "API_PORT" and value:
                try:
                    self.config["api"]["port"] = int(value)
                except ValueError:
                    logger.warning(f"Invalid port value: {value}")
            elif var == "DEBUG" and value:
                self.config["api"]["debug"] = value.lower() == "true"
                
    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """Deep merge two dictionaries."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
                
    def _validate_config(self) -> None:
        """Validate configuration."""
        # Check for required environment variables
        for var in self.REQUIRED_ENV_VARS:
            if var == "OPENAI_API_KEY" and not hasattr(self, "openai_api_key"):
                logger.warning(f"Required environment variable {var} not set")
                
        # Validate embedding configuration
        if "embedding" in self.config:
            if self.config["embedding"]["model"] not in [
                "text-embedding-ada-002", 
                "text-embedding-3-small", 
                "text-embedding-3-large"
            ]:
                logger.warning(f"Unknown embedding model: {self.config['embedding']['model']}")
                
        # Validate vector DB configuration
        if "vector_db" in self.config:
            if self.config["vector_db"]["distance_metric"] not in ["cosine", "euclidean", "dot"]:
                logger.warning(f"Unknown distance metric: {self.config['vector_db']['distance_metric']}")
                
    def _configure_logging(self) -> None:
        """Configure logging based on settings."""
        log_level = getattr(logging, self.config["logging"]["level"], logging.INFO)
        log_format = self.config["logging"]["format"]
        log_file = self.config["logging"]["file"]
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=log_file
        )
        
    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Optional key within section
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        if section not in self.config:
            return default
            
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key, default)
        
    def get_openai_api_key(self) -> str:
        """
        Get OpenAI API key.
        
        Returns:
            OpenAI API key
            
        Raises:
            ConfigurationError: If API key not found
        """
        if hasattr(self, "openai_api_key"):
            return self.openai_api_key
            
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            return api_key
            
        raise ConfigurationError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
    def get_database_url(self) -> Optional[str]:
        """
        Get database URL.
        
        Returns:
            Database URL or None
        """
        # First check database section
        uri = self.get("database", "uri")
        if uri:
            return uri
            
        # Then check environment variable
        return os.environ.get("DATABASE_URL")
        
    def to_dict(self) -> Dict:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary (without secrets)
        """
        return self.config.copy()

# Create global config instance
config = EnhancedConfig()

def get_config() -> EnhancedConfig:
    """
    Get global configuration instance.
    
    Returns:
        EnhancedConfig instance
    """
    return config