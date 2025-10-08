"""
Tests for main ToolCallingAgent functionality
"""
import pytest
from unittest.mock import MagicMock


def test_tool_calling_agent_initialization():
    """Test ToolCallingAgent initialization"""
    from local_llm_serving.main import ToolCallingAgent

    # Test initialization - should always use Ollama
    agent = ToolCallingAgent()
    assert agent.backend_type == 'ollama'


def test_backend_detection():
    """Test that only Ollama backend is supported"""
    from local_llm_serving.main import ToolCallingAgent

    # All initializations should result in Ollama backend
    agent = ToolCallingAgent()
    assert agent.backend_type == 'ollama'


def test_streaming_response():
    """Test streaming response functionality"""
    from local_llm_serving.main import ToolCallingAgent

    # Create agent and mock its internal agent
    agent = ToolCallingAgent()
    mock_agent_instance = MagicMock()
    mock_agent_instance.chat.return_value = iter(["test ", "response"])
    agent.agent = mock_agent_instance

    response = list(agent.chat("test message", stream=True))
    assert response == ["test ", "response"]


def test_non_streaming_response():
    """Test non-streaming response functionality"""
    from local_llm_serving.main import ToolCallingAgent

    # Create agent and mock its internal agent
    agent = ToolCallingAgent()
    mock_agent_instance = MagicMock()
    mock_agent_instance.chat.return_value = "test response"
    agent.agent = mock_agent_instance

    response = agent.chat("test message", stream=False)
    assert response == "test response"


def test_tool_execution():
    """Test tool execution through main agent"""
    from local_llm_serving.main import ToolCallingAgent

    # Create agent and mock its internal agent
    agent = ToolCallingAgent()
    mock_agent_instance = MagicMock()
    mock_agent_instance.chat.return_value = "Weather in Paris is 22°C"
    agent.agent = mock_agent_instance

    response = agent.chat("What's the weather in Paris?")
    assert "Paris" in response


def test_error_handling():
    """Test error handling in main agent"""
    from local_llm_serving.main import ToolCallingAgent

    # Create agent and mock its internal agent
    agent = ToolCallingAgent()
    mock_agent_instance = MagicMock()
    mock_agent_instance.chat.side_effect = Exception("Test error")
    agent.agent = mock_agent_instance

    try:
        response = agent.chat("test message")
        # If no exception is raised, the error should be handled gracefully
        assert "error" in response.lower() or "Error" in response or "exception" in response.lower()
    except Exception as e:
        # If an exception is raised, that's also valid error handling
        assert "test error" in str(e).lower()