"""
hands_on_ai: Your Hands-on AI Toolkit

A modular toolkit for learning AI concepts through hands-on experimentation.
"""

__version__ = "0.1.6"

# Import core modules
from . import chat
from . import rag
from . import agent
from . import config

# Import Colab utilities
from .colab_utils import is_colab, setup_colab, load_colab_config

# Make modules available at top level
__all__ = [
    "chat",
    "rag", 
    "agent",
    "config",
    "is_colab",
    "setup_colab",
    "load_colab_config"
]

# Auto-load Colab settings if available
if is_colab():
    load_colab_config()
