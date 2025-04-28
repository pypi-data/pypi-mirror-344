# HandsOnAI: Your AI Learning Lab

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/licence-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Classroom Ready](https://img.shields.io/badge/classroom-ready-brightgreen.svg)]()
[![Beginner Friendly](https://img.shields.io/badge/beginner-friendly-orange.svg)]()

> AI learning made simple for students and educators

HandsOnAI is a unified educational toolkit designed to teach students how modern AI systems work — by building and interacting with them directly.

It provides a clean, modular structure that introduces core AI concepts progressively through three tools:

## 🧱 Module Overview

| Module | Purpose | CLI Name |
|--------|---------|----------|
| chat | Simple chatbot with system prompts | chat |
| rag | Retrieval-Augmented Generation (RAG) | rag |
| agent | ReAct-style reasoning with tool use | agent |

Each module is:
- 🔌 Self-contained
- 🧩 Installable via one package: `pip install hands-on-ai`
- 🧠 Designed for progressive learning

## 🗂 Project Structure

```
hands_on_ai/
├── chat/           ← A simple prompt/response chatbot
├── rag/            ← Ask questions using your own documents
├── agent/          ← Agent reasoning + tools (ReAct-style)
├── config.py       ← Shared config (model, chunk size, paths)
├── cli.py          ← Meta CLI (list, config, version)
└── utils/          ← Shared tools, prompts, paths, etc.
```

## 🧑‍🏫 Why This Matters for Students

Each tool teaches a different level of modern AI interaction:

- **chat** – Prompt engineering, roles, and LLMs
- **rag** – Document search, embeddings, and grounded answers
- **agent** – Multi-step reasoning, tool use, and planning

## 🚀 Getting Started

### Installation

```bash
# Install from PyPI
pip install hands-on-ai

# Or directly from GitHub
pip install git+https://github.com/teaching-repositories/hands-on-ai.git
```

### Prerequisites

- Python 3.6 or higher
- For local LLM usage: [Ollama](https://ollama.ai/) or similar local LLM server

### API Key Configuration

#### Environment Variable
Set the API key using the environment variable:
```bash
export HANDS_ON_AI_API_KEY=your_api_key_here
```

#### In Code
```python
from hands_on_ai import setup_colab

# Configure for Colab or local use
setup_colab(
    server_url="https://your-ollama-server.com",
    model="your-model-name",
    api_key="your_api_key_here"
)
```

### Package Building and Publishing

#### Using uv for Package Management

##### Build the Package
```bash
# Install build dependencies
uv pip install build twine

# Build the distribution files
uv run python -m build

# Check the distribution files
ls dist/
```

##### Publish to PyPI
```bash
# Make sure you have a PyPI account and have generated an API token
uv run python -m twine upload dist/*
```

##### Development Workflow
```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows

# Install development dependencies
uv pip install -e .[dev]
```

### Quick Start

Run a local Ollama server, then import and start chatting:

```python
from hands_on_ai.chat import pirate_bot
print(pirate_bot("What is photosynthesis?"))
```

For more options:

```python
from hands_on_ai.chat import get_response, friendly_bot, pirate_bot

# Basic usage with default model
response = get_response("Tell me about planets")
print(response)

# Use a personality bot
pirate_response = pirate_bot("Tell me about sailing ships")
print(pirate_response)
```

## Security Notes
- Never commit API keys to version control
- Use environment variables or secure configuration management
- Implement proper access controls on your Ollama server

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## LLM Ready

This package is LLM-ready with a comprehensive guide for Large Language Models to understand its functionality. See the [LLM Guide](docs/llm-guide.md) for detailed API references, usage examples, and best practices.

For best results when working with an LLM:
1. Download the LLM guide file
2. Upload it to your LLM interface/chat at the beginning of your conversation
3. The LLM will now have detailed knowledge about the package's structure and capabilities

## Acknowledgments

- Built with education in mind
- Powered by open-source LLM technology
- Inspired by educators who want to bring AI into the classroom responsibly