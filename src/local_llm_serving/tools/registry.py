"""
Tool registry for managing available tools
"""
import json
from typing import Dict, Any, List
from .implementations import (
    get_current_temperature,
    get_current_time,
    convert_currency,
    execute_python_code,
    parse_pdf_content,
    get_random_number
)


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self.tools = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools"""
        self.register_tool(
            name="get_current_temperature",
            function=get_current_temperature,
            description="Get the current temperature for a specific location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country, e.g., 'Paris, France'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use (by default, celsius)"
                    }
                },
                "required": ["location", "unit"]
            }
        )

        self.register_tool(
            name="get_current_time",
            function=get_current_time,
            description="Get the current date and time in a specific timezone",
            parameters={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone name (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo'). Use standard IANA timezone names.",
                        "default": "UTC"
                    }
                },
                "required": []
            }
        )

        self.register_tool(
            name="convert_currency",
            function=convert_currency,
            description="Convert an amount from one currency to another. You MUST use this tool to convert currencies in order to get the latest exchange rate.",
            parameters={
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "Source currency code (e.g., 'USD', 'EUR')"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Target currency code (e.g., 'USD', 'EUR')"
                    }
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        )

        self.register_tool(
            name="code_interpreter",
            function=execute_python_code,
            description="Execute Python code for calculations and data processing. You MUST use this tool to perform any complex calculations or data processing.",
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )

        self.register_tool(
            name="parse_pdf",
            function=parse_pdf_content,
            description="Parse and extract text content from a PDF file",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL or file path to the PDF document"
                    }
                },
                "required": ["url"]
            }
        )

        self.register_tool(
            name="get_random_number",
            function=get_random_number,
            description="Generate a random number within a specified range",
            parameters={
                "type": "object",
                "properties": {
                    "min_val": {
                        "type": "integer",
                        "description": "Minimum value (default: 1)",
                        "default": 1
                    },
                    "max_val": {
                        "type": "integer",
                        "description": "Maximum value (default: 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        )

    def register_tool(self, name: str, function: callable, description: str, parameters: Dict):
        """Register a new tool"""
        self.tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters
        }

    def get_tool_schemas(self) -> List[Dict]:
        """Get OpenAI-compatible tool schemas"""
        schemas = []
        for name, tool in self.tools.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return schemas

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name with given arguments"""
        if name not in self.tools:
            return json.dumps({"error": f"Tool '{name}' not found"})

        try:
            result = self.tools[name]["function"](**arguments)
            return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        except Exception as e:
            return json.dumps({"error": str(e)})


def format_tool_response(tool_name: str, tool_result: str) -> Dict:
    """Format tool response for the chat model"""
    return {
        "role": "tool",
        "name": tool_name,
        "content": tool_result
    }