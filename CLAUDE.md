# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Universal Tool Calling Demo that demonstrates LLM tool calling across Windows, macOS, and Linux using Ollama for universal compatibility with OpenAI-compatible tool calling and streaming support.

## Development Commands

### Environment Setup
```bash
# Install dependencies and sync environment
uv sync

# Check system compatibility
uv run python -m local_llm_serving.utils.compatibility

# Run comprehensive setup (includes Python/CUDA checks)
uv run bash scripts/setup.sh
```

### Running the Application
```bash
# Run with CLI
uv run llm-serve

# Run specific modes
uv run llm-serve --mode examples      # Examples only
uv run llm-serve --mode interactive   # Interactive chat
uv run llm-serve --no-stream          # Disable streaming

# Show system info
uv run llm-serve --info
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_main.py -v

# Run tests with coverage
uv run pytest tests/ --cov=src/local_llm_serving

# Run streaming tests
uv run pytest tests/test_streaming.py -v

# Run single test by name
uv run pytest -k "test_tool_calling"

# Test specific tools
uv run python scripts/test_weather.py
uv run python scripts/test_code_interpreter_full.py

# Run streaming demo
uv run python scripts/demo_streaming.py
```

### Code Quality
```bash
# Format code with black
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Check types (if mypy configured)
uv run mypy src/local_llm_serving/
```

## Architecture Overview

### High-Level Design
The system uses a **universal Ollama-based architecture**:
1. `ToolCallingAgent` in `main.py` uses Ollama for all platforms
2. Ollama provides consistent OpenAI-compatible tool calling format
3. Streaming architecture provides real-time tool execution feedback
4. Universal compatibility across Windows, macOS, and Linux

### Core Components

**Entry Point (`src/local_llm_serving/main.py`)**
- `ToolCallingAgent` class handles backend selection and unified interface
- CLI argument parsing and mode selection
- Streaming/non-streaming response handling

**Backend Implementation (`src/local_llm_serving/agents/`)**
- `ollama_agent.py`: Native Ollama integration with OpenAI compatibility
- Implements streaming and tool calling interfaces

**Tool System (`src/local_llm_serving/tools/`)**
- `registry.py`: Central tool registry with OpenAI function format
- `implementations.py`: Built-in tools (weather, time, currency, code, PDF)
- Tools execute in sandboxed environment with proper error handling


### Architecture Notes
- **Ollama Only**: Simplified architecture using Ollama across all platforms
- **OpenAI Compatibility**: Ollama provides OpenAI-compatible API for tool calling
- **Universal Setup**: Same installation and configuration for all platforms

### Tool Calling Architecture
- **OpenAI-compatible format**: Standard function calling schema
- **ReAct pattern**: Reasoning → Tool Selection → Execution → Response
- **Streaming chunks**: thinking (gray), tool_call (blue), tool_result (green), content (white)
- **Error handling**: Graceful fallbacks and user-friendly messages

### Key Design Patterns
1. **Strategy Pattern**: Backend selection based on capabilities
2. **Registry Pattern**: Tool registration and discovery
3. **Observer Pattern**: Streaming response chunks
4. **Factory Pattern**: Agent creation with configuration

## Platform-Specific Setup

### macOS
```bash
brew install ollama
ollama serve                    # Start in separate terminal
ollama pull qwen3:0.6b         # Default model
```

### Windows
- Download Ollama from https://ollama.com/download/windows
- Start Ollama service, then: `ollama pull qwen3:0.6b`

### Linux
```bash
# With GPU: Install CUDA toolkit, vLLM auto-detected
# Without GPU:
curl -fsSL https://ollama.com/install.sh | sh
systemctl start ollama
ollama pull qwen3:0.6b
```

## Configuration

Environment variables (`.env` file):
- `MODEL_NAME`: Model to use (default: qwen3:0.6b)
- `OLLAMA_HOST`: Ollama server host (default: localhost)
- `OLLAMA_PORT`: Ollama server port (default: 11434)
- `LOG_LEVEL`: Logging level (default: INFO)

## Adding Custom Tools

```python
from local_llm_serving.tools.registry import ToolRegistry

def my_custom_tool(param1: str, param2: int) -> str:
    """Your tool implementation"""
    return f"Processed {param1} with {param2}"

registry = ToolRegistry()
registry.register_tool(
    name="my_custom_tool",
    function=my_custom_tool,
    description="Description of what the tool does",
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

## Important Notes

- Always use `uv run` for Python commands to ensure proper environment
- Ollama must be running as a service before starting the application
- Default model (qwen3:0.6b) is optimized for tool calling with small footprint
- Streaming shows internal reasoning - disable with `--no-stream` for cleaner output
- Tool execution happens in sandboxed environment with timeout protection