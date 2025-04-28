"""Configuration management for Hands-On AI package."""

import os
import logging
import random

# Set up logging
log = logging.getLogger(__name__)

# Default configuration values
DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_MODEL = "llama2"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 256

# Custom exception for API key issues
class APIKeyError(Exception):
    """Raised when there are issues with API key configuration."""
    pass

# Fallback models list
DEFAULT_FALLBACK_MODELS = [
    "llama2",
    "mistral",
    "gemma"
]

def load_fallbacks():
    """
    Load fallback models for the AI system.
    
    Returns:
        list: A list of fallback model names
    """
    # Check environment variable for custom fallbacks
    env_fallbacks = os.environ.get("HANDS_ON_AI_FALLBACK_MODELS")
    
    if env_fallbacks:
        return env_fallbacks.split(",")
    
    return DEFAULT_FALLBACK_MODELS

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
            "fallback_models": load_fallbacks()
        }
    except Exception as e:
        log.warning(f"Failed to read default config: {e}")
        return {
            "server": DEFAULT_SERVER,
            "model": DEFAULT_MODEL,
            "embedding_model": DEFAULT_EMBEDDING_MODEL,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "api_key": None,
            "fallback_models": DEFAULT_FALLBACK_MODELS
        }

def load_config():
    """Load configuration from config file or environment variables."""
    # Start with default configuration
    config = load_default_config()
    
    # Prioritize environment variables and Colab userdata
    try:
        # Try to import Colab userdata if available
        from google.colab import userdata
        
        # Check Colab userdata first
        colab_api_key = userdata.get("HANDS_ON_AI_API_KEY", None)
        if colab_api_key:
            config["api_key"] = colab_api_key
    except ImportError:
        # Not in Colab, continue with other methods
        pass
    
    # Check environment variables
    if "HANDS_ON_AI_SERVER" in os.environ:
        config["server"] = os.environ["HANDS_ON_AI_SERVER"]
    
    if "HANDS_ON_AI_MODEL" in os.environ:
        config["model"] = os.environ["HANDS_ON_AI_MODEL"]
    
    if "HANDS_ON_AI_EMBEDDING_MODEL" in os.environ:
        config["embedding_model"] = os.environ["HANDS_ON_AI_EMBEDDING_MODEL"]
    
    if "HANDS_ON_AI_API_KEY" in os.environ:
        config["api_key"] = os.environ["HANDS_ON_AI_API_KEY"]
    
    return config

def validate_api_key(api_key):
    """
    Validate the API key.
    
    Args:
        api_key (str): API key to validate
    
    Raises:
        APIKeyError: If the API key is invalid
    """
    if not api_key:
        raise APIKeyError("No API key provided")
    
    # Basic validation - can be expanded
    if len(api_key.strip()) < 10:
        raise APIKeyError("API key appears to be too short")
    
    # Additional validation can be added here
    # For example, checking for specific formats, making a test request, etc.

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
    """
    Retrieve the API key from configuration.
    
    Returns:
        str or None: API key if configured, None otherwise
    
    Raises:
        APIKeyError: If API key is invalid
    """
    config = load_config()
    api_key = config.get("api_key")
    
    try:
        validate_api_key(api_key)
    except APIKeyError as e:
        log.warning(f"API Key Validation Error: {e}")
        return None
    
    return api_key

def select_model(fallback=True):
    """
    Select a model, with optional fallback support.
    
    Args:
        fallback (bool): Whether to use fallback models if primary model fails
    
    Returns:
        str: Selected model name
    """
    config = load_config()
    
    if not fallback:
        return config['model']
    
    # Get list of fallback models
    fallback_models = config.get('fallback_models', DEFAULT_FALLBACK_MODELS)
    
    # Shuffle fallback models to distribute load
    random.shuffle(fallback_models)
    
    # Always include the primary model at the start
    all_models = [config['model']] + [
        model for model in fallback_models 
        if model != config['model']
    ]
    
    return all_models[0]
