# Universal Tool Calling Demo

A cross-platform demonstration of LLM tool calling using Ollama. Works seamlessly on Windows, macOS, and Linux with a unified, simple setup.

> **Fork Source**: This project is a fork of [ai-agent-book-projects/week2/local_llm_serving](https://github.com/bojieli/ai-agent-book-projects/tree/main/week2/local_llm_serving) by bojieli, refactored to use modern Python packaging with uv and improved project structure.

## 🌟 Features

- **Universal Compatibility**: Single entry point that works on all platforms
- **Simple Setup**: Uses **Ollama** for easy installation and cross-platform support
- **Standard Tool Calling**: Uses OpenAI-compatible tool calling format
- **Built-in Tools**: Weather, calculator, time, and easy to add custom tools
- **Interactive & Example Modes**: Test with examples or chat interactively
- **🆕 Streaming Support**: Real-time display of thinking process, tool calls, and responses

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository>
cd local_llm_serving

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install the package with dependencies
uv sync

# 4. Run the main script
uv run llm-serve
```

That's it! The script uses Ollama for universal compatibility.

## 📋 Prerequisites

### All Platforms
- Python 3.10+
- [uv package manager](https://docs.astral.sh/uv/) (recommended for fast, reliable installs)
- `uv pip install -r requirements.txt`

### Platform-Specific Setup

#### 🍎 macOS
```bash
# Install Ollama
brew install ollama

# Start Ollama service (in separate terminal)
ollama serve

# Download a model
ollama pull qwen3:0.6b
```

#### 🪟 Windows
```bash
# Download and install Ollama
# From: https://ollama.com/download/windows

# Pull a model
ollama pull qwen3:0.6b
```

#### 🐧 Linux
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start service
systemctl start ollama

# Pull a model
ollama pull qwen3:0.6b
```

## 🎮 Usage

### Basic Usage

```bash
# Run the application
uv run llm-serve

# Run examples only
uv run llm-serve --mode examples

# Run interactive mode only
uv run llm-serve --mode interactive

# Show system info
uv run llm-serve --info
```

### Using in Your Code

```python
from local_llm_serving.main import ToolCallingAgent

# Initialize (auto-detects best backend)
agent = ToolCallingAgent()

# Send a message
response = agent.chat("What's the weather in Tokyo?")
print(response)

# Disable tools for a query
response = agent.chat("Tell me a joke", use_tools=False)

# Reset conversation
agent.reset_conversation()
```

### Adding Custom Tools

```python
from local_llm_serving.tools.registry import ToolRegistry

# Get the tool registry
registry = ToolRegistry()

# Define your tool function
def my_custom_tool(param1: str, param2: int) -> str:
    return f"Processed {param1} with {param2}"

# Register it
registry.register_tool(
    name="my_custom_tool",
    function=my_custom_tool,
    description="My custom tool description",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "First parameter"},
            "param2": {"type": "integer", "description": "Second parameter"}
        },
        "required": ["param1", "param2"]
    }
)
```

## 📁 Project Structure

```
local_llm_serving/
├── src/local_llm_serving/     # Main Python package
│   ├── main.py                # Entry point with ToolCallingAgent
│   ├── config.py              # Configuration management
│   ├── agents/                # Agent implementations
│   │   └── ollama_agent.py    # Ollama implementation
│   ├── tools/                 # Tool registry and implementations
│   │   ├── registry.py        # ToolRegistry class
│   │   └── implementations.py # Individual tool functions
│   └── utils/                 # Utilities
│       └── compatibility.py   # Platform detection
├── tests/                     # Test suite
├── scripts/                   # Demo and utility scripts
├── pyproject.toml             # Package configuration and dependencies
├── uv.lock                    # Lock file for reproducible builds
└── README.md                  # This file
```

## 🛠️ Available Tools

1. **get_current_temperature**: Get real-time weather information using [Open-Meteo API](https://open-meteo.com/) (no API key required)
2. **get_current_time**: Get current time in different timezones
3. **convert_currency**: Convert between different currencies (simulated rates)
4. **parse_pdf**: Parse PDF documents from URL or local file
5. **code_interpreter**: Execute Python code for complex calculations and data processing

## 🎬 Streaming Mode

The agents now support streaming responses, which displays:
- 🧠 **Internal thinking** process (shown in gray)
- 🔧 **Tool calls** as they happen
- ✓ **Tool results** in real-time
- 📝 **Final response** streamed character by character

### Using Streaming

#### Interactive Mode (Default)
```bash
# Streaming is enabled by default
python main.py

# Disable streaming
python main.py --no-stream

# Toggle streaming during chat with /stream command
```

#### Programmatic Usage
```python
from local_llm_serving.main import ToolCallingAgent

# Initialize agent
agent = ToolCallingAgent()

# Stream response
for chunk in agent.chat("What's the weather in Tokyo?", stream=True):
    chunk_type = chunk.get("type")
    content = chunk.get("content", "")

    if chunk_type == "thinking":
        print(f"Thinking: {content}")
    elif chunk_type == "tool_call":
        print(f"Tool: {content['name']}")
    elif chunk_type == "tool_result":
        print(f"Result: {content}")
    elif chunk_type == "content":
        print(content, end="", flush=True)
```

### Test Streaming
```bash
# Run streaming demo
uv run python scripts/demo_streaming.py

# Run streaming tests
uv run pytest tests/test_streaming.py -v
```

## 🔧 Configuration

Copy `env.example` to `.env` and customize:

```bash
# For vLLM (if you have GPU)
MODEL_NAME=Qwen/Qwen3-0.6B
VLLM_HOST=localhost
VLLM_PORT=8000

# Logging
LOG_LEVEL=INFO
```

## 🛠️ Development Setup

For developers working on this project:

```bash
# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/

# Run tests with coverage
uv run pytest tests/ --cov=src/local_llm_serving

# Run specific test file
uv run pytest tests/test_main.py -v

# Install pre-commit hooks (if available)
uv run pre-commit install
```

The project uses:
- **uv** for fast, reliable package management
- **pytest** for testing
- **src/** layout for proper Python packaging
- **pyproject.toml** for modern dependency management

## 📊 Tool Calling Format

This project uses **standard OpenAI-compatible tool calling**:

```json
{
  "tool_calls": [{
    "id": "call_123",
    "type": "function",
    "function": {
      "name": "get_weather",
      "arguments": {"location": "Tokyo"}
    }
  }]
}
```

No ad-hoc parsing or custom formats - just the standard that works across platforms.

## 🐛 Troubleshooting

### "Ollama not found"
- **Mac**: `brew install ollama && ollama serve`
- **Windows**: Download from [ollama.com](https://ollama.com/download/windows)
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`

### "No models installed"
```bash
ollama pull qwen3:0.6b  # Default model used by this project
```

## 🤝 Supported Models

### Default Model:
- **Qwen3** (0.6B) - Default model used by this project. Small size with decent tool calling support.

### Other Compatible Models for Tool Calling:
- **Qwen3** (8B+) - Good tool support
- **Llama 3.1/3.2** (8B+) - Good tool support
- **Mistral Nemo** - Great tool calling

All models are available through Ollama for easy installation and management.

## 📚 How It Works

1. **Universal Setup**: Uses Ollama for consistent experience across all platforms
2. **Tool Execution**: Uses standard OpenAI-compatible tool calling format
3. **Response Generation**: Tools are executed and results fed back to the model

## 🔗 References

- [Ollama Documentation](https://ollama.com/)
- [OpenAI Tool Calling](https://platform.openai.com/docs/guides/function-calling)

## 📄 License

This demo project is provided as-is for educational purposes.

## 🔄 Recent Updates

### v2.0 - Modern Python Packaging Refactor
- **Migrated to uv**: Faster, more reliable package management
- **Proper Python packaging**: Now uses src/ layout with pyproject.toml
- **All tests passing**: Comprehensive test suite with pytest
- **Improved imports**: Clean package structure with `local_llm_serving.*`
- **CLI integration**: Installable as `llm-serve` command
- **Development friendly**: Easy setup with `uv pip install -e ".[dev]"`

The project maintains full backward compatibility while adopting modern Python best practices.