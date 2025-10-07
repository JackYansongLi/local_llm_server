# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Universal Tool Calling Demo that demonstrates LLM tool calling functionality across Windows, macOS, and Linux. The project automatically selects the best backend (vLLM for GPU systems, Ollama for CPU systems) and provides OpenAI-compatible tool calling with streaming support.

## Development Commands

### Environment Setup
```bash
# Check system compatibility
python check_compatibility.py

# Install dependencies (use UV package manager)
uv pip install -r requirements.txt

# Run setup script for comprehensive environment setup
./setup.sh
```

### Running the Application
```bash
# Auto-detect best backend and run
python main.py

# Force specific backend
python main.py --backend ollama    # Force Ollama
python main.py --backend vllm      # Force vLLM (requires GPU)

# Run with specific modes
python main.py --mode examples      # Run examples only
python main.py --mode interactive   # Run interactive mode only
python main.py --no-stream          # Disable streaming

# Show system info
python main.py --info
```

### Testing
```bash
# Test streaming functionality
python test_streaming.py

# Test specific tools
python test_weather.py
python test_code_interpreter_full.py

# Run streaming demo
python demo_streaming.py
```

## Architecture Overview

### Core Components

1. **main.py** - Universal entry point with automatic backend detection
   - `ToolCallingAgent` class handles platform detection and backend selection
   - Supports both streaming and non-streaming modes
   - Integrates with both vLLM and Ollama backends

2. **agent.py** - vLLM-specific implementation
   - Manages vLLM server lifecycle
   - Handles OpenAI-compatible tool calling format
   - Implements streaming responses

3. **ollama_native.py** - Ollama-specific implementation
   - Native Ollama tool calling support
   - Streaming implementation for Ollama backend

4. **tools.py** - Tool registry and implementations
   - `ToolRegistry` class manages available tools
   - Built-in tools: weather, time, currency conversion, PDF parsing, code interpreter
   - Tools follow OpenAI function calling format

5. **server.py** - vLLM server management
   - Handles vLLM server startup/shutdown
   - Configures Hermes tool parser
   - Manages server lifecycle

6. **config.py** - Configuration management
   - Model settings (default: Qwen/Qwen3-0.6B)
   - vLLM server configuration
   - Tool enablement flags
   - Logging configuration

### Backend Selection Logic

The system automatically selects the optimal backend:
- **Linux/Windows + NVIDIA GPU** → vLLM (high-performance GPU inference)
- **macOS/No GPU** → Ollama (local CPU inference)

### Tool Calling Format

Uses standard OpenAI-compatible function calling format:
```json
{
  "tool_calls": [{
    "id": "call_123",
    "type": "function",
    "function": {
      "name": "tool_name",
      "arguments": {"param": "value"}
    }
  }]
}
```

### Streaming Architecture

Streaming responses include multiple chunk types:
- `thinking` - Internal reasoning process (gray text)
- `tool_call` - Tool execution notifications
- `tool_result` - Tool execution results
- `content` - Final response content

## Key Dependencies

- **vLLM** (≥0.6.0) - GPU-based LLM inference
- **Ollama** (≥0.1.0) - Local LLM inference
- **FastAPI** (≥0.104.0) - API framework for vLLM server
- **Transformers** (≥4.36.0) - Model handling
- **PyTorch** (≥2.0.0) - Deep learning framework

## Platform-Specific Requirements

### macOS
```bash
brew install ollama
ollama serve                    # Start in separate terminal
ollama pull qwen3:0.6b         # Download model
```

### Windows (No GPU)
- Download Ollama from https://ollama.com/download/windows
- `ollama pull qwen3:0.6b`

### Linux (No GPU)
```bash
curl -fsSL https://ollama.com/install.sh | sh
systemctl start ollama
ollama pull qwen3:0.6b
```

## Configuration

Environment variables (`.env` file):
- `MODEL_NAME` - Model to use (default: Qwen/Qwen3-0.6B)
- `VLLM_HOST` - vLLM server host (default: localhost)
- `VLLM_PORT` - vLLM server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)

## Adding Custom Tools

```python
from tools import ToolRegistry

registry = ToolRegistry()

def my_tool(param: str) -> str:
    return f"Processed {param}"

registry.register_tool(
    name="my_tool",
    function=my_tool,
    description="My custom tool",
    parameters={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Input parameter"}
        },
        "required": ["param"]
    }
)
```

## Important Notes

- Always check system compatibility with `python check_compatibility.py` first
- vLLM requires NVIDIA GPU with CUDA support
- Ollama must be running as a service for Ollama backend
- Default model (Qwen3-0.6B) is optimized for tool calling
- Streaming is enabled by default but can be disabled with `--no-stream`
- uv python xxx.py, remember that I am using uv!