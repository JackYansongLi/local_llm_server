"""
Tests for main ToolCallingAgent functionality
"""
import pytest
from unittest.mock import patch, MagicMock


def test_tool_calling_agent_initialization():
    """Test ToolCallingAgent initialization"""
    from local_llm_serving.main import ToolCallingAgent

    # Test with auto-detection
    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        mock_detect.return_value = 'ollama'
        agent = ToolCallingAgent()
        assert agent.backend_type == 'ollama'

    # Test with forced backend - expect fallback to Ollama since vLLM server isn't running
    agent = ToolCallingAgent(backend='vllm')
    # Since vLLM server isn't running, it should fall back to Ollama
    assert agent.backend_type == 'ollama'  # Fallback behavior


def test_backend_detection():
    """Test backend detection logic"""
    from local_llm_serving.main import ToolCallingAgent

    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        # Test macOS detection
        mock_detect.return_value = 'ollama'
        agent = ToolCallingAgent()
        assert agent.backend_type == 'ollama'

        # Test Linux detection
        mock_detect.return_value = 'ollama'
        agent = ToolCallingAgent()
        assert agent.backend_type == 'ollama'


def test_streaming_response():
    """Test streaming response functionality"""
    from local_llm_serving.main import ToolCallingAgent

    # Mock the _detect_best_backend to return ollama to avoid fallback issues
    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        mock_detect.return_value = 'ollama'

        # Create agent and mock its internal agent
        agent = ToolCallingAgent(backend='ollama')
        mock_agent_instance = MagicMock()
        mock_agent_instance.chat.return_value = iter(["test ", "response"])
        agent.agent = mock_agent_instance

        response = list(agent.chat("test message", stream=True))
        assert response == ["test ", "response"]


def test_non_streaming_response():
    """Test non-streaming response functionality"""
    from local_llm_serving.main import ToolCallingAgent

    # Mock the _detect_best_backend to return ollama to avoid fallback issues
    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        mock_detect.return_value = 'ollama'

        # Create agent and mock its internal agent
        agent = ToolCallingAgent(backend='ollama')
        mock_agent_instance = MagicMock()
        mock_agent_instance.chat.return_value = "test response"
        agent.agent = mock_agent_instance

        response = agent.chat("test message", stream=False)
        assert response == "test response"


def test_tool_execution():
    """Test tool execution through main agent"""
    from local_llm_serving.main import ToolCallingAgent

    # Mock the _detect_best_backend to return ollama to avoid fallback issues
    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        mock_detect.return_value = 'ollama'

        # Create agent and mock its internal agent
        agent = ToolCallingAgent(backend='ollama')
        mock_agent_instance = MagicMock()
        mock_agent_instance.chat.return_value = "Weather in Paris is 22°C"
        agent.agent = mock_agent_instance

        response = agent.chat("What's the weather in Paris?")
        assert "Paris" in response


def test_error_handling():
    """Test error handling in main agent"""
    from local_llm_serving.main import ToolCallingAgent

    # Mock the _detect_best_backend to return ollama to avoid fallback issues
    with patch('local_llm_serving.main.ToolCallingAgent._detect_best_backend') as mock_detect:
        mock_detect.return_value = 'ollama'

        # Create agent and mock its internal agent
        agent = ToolCallingAgent(backend='ollama')
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