"""
Tool implementations for the local LLM serving package
"""
import json
import math
import random
import io
import contextlib
from typing import Dict, Any, List
from datetime import datetime
import requests
from io import BytesIO
import PyPDF2


def get_current_temperature(location: str, unit: str = "celsius") -> str:
    """Get the current temperature for a specific location"""
    try:
        import weather

        # Extract city from location
        city = location.split(",")[0].strip()

        # Get weather data
        w = weather.Weather()
        location_data = w.location(city)
        condition = location_data.condition()
        temp = condition.temp

        # Convert temperature if needed
        if unit.lower() == "fahrenheit":
            temp = temp * 9/5 + 32
            unit_symbol = "°F"
        else:
            unit_symbol = "°C"

        return f"The current temperature in {location} is {temp:.1f}{unit_symbol}"
    except Exception as e:
        return f"Unable to get temperature for {location}: {str(e)}"


def get_current_time(timezone: str = "UTC") -> str:
    """Get the current date and time in a specific timezone"""
    try:
        # For simplicity, we'll use UTC and common timezone offsets
        from datetime import datetime, timezone, timedelta

        # Map common timezone names to offsets
        timezone_offsets = {
            "UTC": 0,
            "EST": -5, "EDT": -4,
            "CST": -6, "CDT": -5,
            "MST": -7, "MDT": -6,
            "PST": -8, "PDT": -7,
            "GMT": 0,
            "CET": 1, "CEST": 2,
            "JST": 9,
            "AEST": 10, "AEDT": 11
        }

        # Get offset or default to UTC
        offset_hours = timezone_offsets.get(timezone.upper(), 0)

        # Create timezone with offset
        tz = timezone(timedelta(hours=offset_hours))

        # Get current time in specified timezone
        now = datetime.now(tz)

        return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Unable to get time for timezone {timezone}: {str(e)}"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency from one type to another"""
    try:
        # Mock exchange rates for demonstration
        exchange_rates = {
            "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "CAD": 1.25, "AUD": 1.35},
            "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0, "CAD": 1.47, "AUD": 1.59},
            "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0, "CAD": 1.71, "AUD": 1.85},
            "JPY": {"USD": 0.0091, "EUR": 0.0078, "GBP": 0.0067, "CAD": 0.011, "AUD": 0.012},
            "CAD": {"USD": 0.80, "EUR": 0.68, "GBP": 0.58, "JPY": 88.0, "AUD": 1.08},
            "AUD": {"USD": 0.74, "EUR": 0.63, "GBP": 0.54, "JPY": 81.0, "CAD": 0.93}
        }

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return f"{amount:.2f} {from_currency} = {amount:.2f} {to_currency}"

        if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
            rate = exchange_rates[from_currency][to_currency]
            converted_amount = amount * rate
            return f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency} (rate: {rate:.4f})"
        else:
            return f"Exchange rate not available for {from_currency} to {to_currency}"
    except Exception as e:
        return f"Unable to convert currency: {str(e)}"


def execute_python_code(code: str) -> Dict[str, Any]:
    """Execute Python code and return structured output"""
    try:
        import re
        import traceback

        # Strip markdown code blocks and other formatting
        code = re.sub(r'^```(?:python|py)?\s*\n', '', code.strip())
        code = re.sub(r'\n```\s*$', '', code)
        code = re.sub(r'^```\s*', '', code)
        code = re.sub(r'\s*```$', '', code)

        # Also strip any leading/trailing whitespace
        code = code.strip()

        # Convert common mathematical notation to Python syntax
        # Replace ^ with ** for exponentiation
        code = re.sub(r'\^', '**', code)

        # Create a full Python namespace with all builtins available
        # This gives the agent access to the complete Python environment
        import sys
        namespace = {
            '__builtins__': __builtins__,
            'math': math,
            'sqrt': math.sqrt,  # Make sqrt directly available
            'random': random,
            'datetime': datetime,
            'sys': sys,
            're': re,
            'json': json
        }

        # Capture both stdout and stderr
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
            exec(code, namespace)

        # Get output and any error messages
        printed_output = output_buffer.getvalue()
        error_output = error_buffer.getvalue()

        # Try to get result from common variable names
        result = namespace.get('result', None)
        if result is None:
            for var_name in ['A', 'total', 'sum', 'output', 'answer', 'final', 'value']:
                if var_name in namespace:
                    result = namespace[var_name]
                    break

        response = {
            "result": result,
            "output": printed_output if printed_output else None,
            "stderr": error_output if error_output else None,
            "success": True
        }

        return response

    except SyntaxError as e:
        error_msg = f"Syntax Error on line {e.lineno}: {e.msg}\n{e.text}"
        return {
            "error": error_msg,
            "error_type": "SyntaxError",
            "success": False
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": error_trace,
            "success": False
        }


def parse_pdf_content(pdf_url: str) -> str:
    """Parse and extract text content from a PDF file"""
    try:
        # Download PDF
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(BytesIO(response.content))

        # Extract text from all pages
        text_content = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content.append(f"Page {page_num + 1}:\n{page.extract_text()}")

        return "\n\n".join(text_content)
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def get_random_number(min_val: int = 1, max_val: int = 100) -> str:
    """Generate a random number within a specified range"""
    try:
        number = random.randint(min_val, max_val)
        return f"Random number between {min_val} and {max_val}: {number}"
    except Exception as e:
        return f"Error generating random number: {str(e)}"