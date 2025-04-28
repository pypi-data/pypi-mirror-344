"""Configuration management for Hands-On AI package."""

import os
import logging

# Default configuration values
DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "llama2"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 256

# Set up logging
log = logging.getLogger(__name__)

def load_default_config():
    """Load the default configuration packaged with HandsOnAI."""
    try:
        # In a real implementation, you might load from a config file
        return {
            "server": DEFAULT_SERVER,
            "model": DEFAULT_MODEL,
            "embedding_model": DEFAULT_EMBEDDING_MODEL,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "api_key": None,  # Add API key to defaults
        }
    except Exception as e:
        log.warning(f"Failed to read default config: {e}")
        return {
            "server": DEFAULT_SERVER,
            "model": DEFAULT_MODEL,
            "embedding_model": DEFAULT_EMBEDDING_MODEL,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "api_key": None,
        }

def load_config():
    """Load configuration from config file or environment variables."""
    # Start with default configuration
    config = load_default_config()
    
    # Override with environment variables if set
    if "HANDS_ON_AI_SERVER" in os.environ:
        config["server"] = os.environ["HANDS_ON_AI_SERVER"]
    
    if "HANDS_ON_AI_MODEL" in os.environ:
        config["model"] = os.environ["HANDS_ON_AI_MODEL"]
    
    if "HANDS_ON_AI_EMBEDDING_MODEL" in os.environ:
        config["embedding_model"] = os.environ["HANDS_ON_AI_EMBEDDING_MODEL"]
    
    if "HANDS_ON_AI_API_KEY" in os.environ:
        config["api_key"] = os.environ["HANDS_ON_AI_API_KEY"]
    
    return config

def get_server_url():
    """Retrieve the server URL from configuration."""
    return load_config()["server"]

def get_model():
    """Retrieve the default model from configuration."""
    return load_config()["model"]

def get_embedding_model():
    """Retrieve the embedding model from configuration."""
    return load_config()["embedding_model"]

def get_chunk_size():
    """Retrieve the chunk size from configuration."""
    return load_config()["chunk_size"]

def get_api_key():
    """Retrieve the API key from configuration."""
    return load_config().get("api_key")
