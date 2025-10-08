"""
Test cases for the cat_file tool
"""
import os
import tempfile
import pytest
from local_llm_serving.tools.implementations import cat_file


class TestCatFile:
    """Test the cat_file tool implementation"""

    def test_read_existing_file(self):
        """Test reading an existing file"""
        # Create a temporary file with test content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "Hello, this is a test file!\nIt has multiple lines."
            f.write(test_content)
            temp_file_path = f.name

        try:
            # Test reading the file
            result = cat_file(temp_file_path)
            assert result == test_content
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_read_empty_file(self):
        """Test reading an empty file"""
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file_path = f.name

        try:
            # Test reading the empty file
            result = cat_file(temp_file_path)
            assert result == ""
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_read_nonexistent_file(self):
        """Test reading a non-existent file"""
        result = cat_file("/path/that/does/not/exist.txt")
        assert "Error reading file" in result

    def test_read_directory_instead_of_file(self):
        """Test attempting to read a directory"""
        # Use the current directory as a test
        result = cat_file("/Users/jackyansongli/git/local_llm_serving/tests")
        assert "Error reading file" in result

    def test_read_file_with_special_characters(self):
        """Test reading a file with special characters"""
        # Create a temporary file with special content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "Special chars: abc123\nNumbers: 123456\nSymbols: !@#$%^&*()"
            f.write(test_content)
            temp_file_path = f.name

        try:
            # Test reading the file
            result = cat_file(temp_file_path)
            assert result == test_content
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_read_binary_file(self):
        """Test reading a binary file (should handle gracefully)"""
        # Create a small binary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
            temp_file_path = f.name

        try:
            # Test reading the binary file
            result = cat_file(temp_file_path)
            # The result should contain the binary data (cat can read binary files)
            assert len(result) > 0
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_integration_with_tool_registry(self):
        """Test that the cat_file tool is properly registered"""
        from local_llm_serving.tools.registry import ToolRegistry

        registry = ToolRegistry()

        # Check that cat_file is in the registry
        assert "cat_file" in registry.tools

        # Check the tool schema
        tool_schema = registry.tools["cat_file"]
        assert tool_schema["description"] == "Read and display the contents of a file using the cat shell command"

        # Check the parameters
        params = tool_schema["parameters"]
        assert params["type"] == "object"
        assert "file_path" in params["properties"]
        assert params["properties"]["file_path"]["type"] == "string"

        # Test execution through registry
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "Registry test content"
            f.write(test_content)
            temp_file_path = f.name

        try:
            result = registry.execute_tool("cat_file", {"file_path": temp_file_path})
            assert test_content in result
        finally:
            os.unlink(temp_file_path)

    def test_openai_compatible_schema(self):
        """Test that the tool produces OpenAI-compatible schema"""
        from local_llm_serving.tools.registry import ToolRegistry

        registry = ToolRegistry()
        schemas = registry.get_tool_schemas()

        # Find the cat_file schema
        cat_schema = None
        for schema in schemas:
            if schema["function"]["name"] == "cat_file":
                cat_schema = schema
                break

        assert cat_schema is not None
        assert cat_schema["type"] == "function"
        assert cat_schema["function"]["name"] == "cat_file"
        assert "file_path" in cat_schema["function"]["parameters"]["properties"]


if __name__ == "__main__":
    # Run a simple test
    test = TestCatFile()
    test.test_read_existing_file()
    test.test_read_nonexistent_file()
    test.test_integration_with_tool_registry()
    print("All tests passed!")