"""
Configuration for Ollama Tool Calling Demo
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:0.6b")  # Default Ollama model
MODEL_PATH = os.getenv("MODEL_PATH", None)  # Optional: local model path

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))

# Tool Configuration
ENABLE_WEATHER_TOOL = True
ENABLE_CALCULATOR_TOOL = True
ENABLE_SEARCH_TOOL = True

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = Path("logs") / "ollama_tool_demo.log"
