"""
Test configuration and fixtures for local-llm-serving tests
"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_tool_registry():
    """Sample tool registry for testing"""
    from local_llm_serving.tools.registry import ToolRegistry
    return ToolRegistry()

@pytest.fixture
def mock_ollama_response():
    """Mock Ollama response for testing"""
    return {
        "message": {
            "content": "Test response",
            "tool_calls": None
        },
        "done": True
    }

@pytest.fixture
def mock_vllm_response():
    """Mock vLLM response for testing"""
    return {
        "choices": [{
            "message": {
                "content": "Test response",
                "tool_calls": None
            }
        }]
    }