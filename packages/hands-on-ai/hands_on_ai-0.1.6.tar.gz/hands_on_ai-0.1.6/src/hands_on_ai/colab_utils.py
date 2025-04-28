"""Utilities for Google Colab integration."""

import os

def is_colab():
    """Check if running in Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def setup_colab(server_url=None, model=None, api_key=None):
    """
    Configure hands-on-ai for use in Google Colab.
    
    Args:
        server_url (str): URL of the Ollama server
        model (str): Name of the default model to use
        api_key (str): API key for server authentication
    """
    if not is_colab():
        print("Not running in Google Colab.")
        return False
    
    # Set environment variables for current session
    if server_url:
        os.environ["HANDS_ON_AI_SERVER"] = server_url
    if model:
        os.environ["HANDS_ON_AI_MODEL"] = model
    if api_key:
        os.environ["HANDS_ON_AI_API_KEY"] = api_key
        
    # Store in userdata for persistence
    try:
        from google.colab import userdata
        if server_url:
            userdata.set("HANDS_ON_AI_SERVER", server_url)
        if model:
            userdata.set("HANDS_ON_AI_MODEL", model)
        if api_key:
            userdata.set("HANDS_ON_AI_API_KEY", api_key)
            
        print("Configuration saved to Colab storage.")
        return True
    except Exception as e:
        print(f"Warning: Could not save to persistent storage: {e}")
        print("Settings will be lost if runtime restarts.")
        return False

def load_colab_config():
    """Load configuration from Colab userdata if available."""
    if not is_colab():
        return False
        
    try:
        from google.colab import userdata
        loaded = False
        
        # Try to load from userdata
        if userdata.get("HANDS_ON_AI_SERVER"):
            os.environ["HANDS_ON_AI_SERVER"] = userdata.get("HANDS_ON_AI_SERVER")
            loaded = True
            
        if userdata.get("HANDS_ON_AI_MODEL"):
            os.environ["HANDS_ON_AI_MODEL"] = userdata.get("HANDS_ON_AI_MODEL")
            loaded = True
            
        if userdata.get("HANDS_ON_AI_API_KEY"):
            os.environ["HANDS_ON_AI_API_KEY"] = userdata.get("HANDS_ON_AI_API_KEY")
            loaded = True
            
        return loaded
    except:
        return False
