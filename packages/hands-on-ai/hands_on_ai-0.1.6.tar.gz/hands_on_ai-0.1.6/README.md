# HandsOnAI: Your AI Learning Lab

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/licence-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Classroom Ready](https://img.shields.io/badge/classroom-ready-brightgreen.svg)]()
[![Beginner Friendly](https://img.shields.io/badge/beginner-friendly-orange.svg)]()

> AI learning made simple for students and educators

HandsOnAI is a unified educational toolkit designed to teach students how modern AI systems work — by building and interacting with them directly.

## 🔐 API Key Configuration

### Environment Variable Method
```bash
# Set API key in your environment
export HANDS_ON_AI_API_KEY=your_secret_api_key_here
```

### In-Code Configuration
```python
from hands_on_ai import setup_colab

# Configure with API key
setup_colab(
    server_url="https://your-ollama-server.com",
    model="llama2",
    api_key="your_secret_api_key_here"
)
```

### Secure API Key Management
```python
# Verify API key configuration
from hands_on_ai.config import get_api_key

api_key = get_api_key()
if api_key:
    print("API key is configured successfully")
else:
    print("No API key found. Please configure.")
```

## 🧱 Module Overview

| Module | Purpose | CLI Name |
|--------|---------|----------|
| chat | Simple chatbot with system prompts | chat |
| rag | Retrieval-Augmented Generation (RAG) | rag |
| agent | ReAct-style reasoning with tool use | agent |

## 🚀 Getting Started

### Installation

```bash
# Install from PyPI
pip install hands-on-ai

# Or directly from GitHub
pip install git+https://github.com/teaching-repositories/hands-on-ai.git
```

### Quick Start

```python
from hands_on_ai.chat import get_response

# Basic usage with API key
response = get_response("Hello, how are you?")
print(response)
```

## 🛡️ Security Best Practices

- Never hardcode API keys in source code
- Use environment variables
- Rotate API keys periodically
- Use secure configuration management

## 📚 Documentation

- [Chat Module Examples](/docs/examples/chat_example.md)
- [RAG Module Examples](/docs/examples/rag_example.md)
- [Agent Module Examples](/docs/examples/agent_example.md)
- [API Key Configuration](/docs/examples/api_key_example.md)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
