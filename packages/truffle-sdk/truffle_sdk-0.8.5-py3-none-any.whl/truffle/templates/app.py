"""
Application template module.
Contains the main application template and related utilities.
"""

from typing import Optional

def get_main_template(app_name: str, description: Optional[str] = None) -> str:
    """
    Get the main application template.
    
    Args:
        app_name: Name of the application
        description: Optional description from -d flag
        
    Returns:
        Formatted template string
    """
    # Use MyApp as default if no name override provided
    class_name = "MyApp" if app_name == "MyTruffleApp" else app_name
    
    # Use provided description or empty with comment
    description_line = f'    description="{description}"' if description else '    description=""  # Add your app description here'
    
    return f'''"""
Truffle App Template
-------------------
IMPORTANT NOTES:
1. All example functions below can be safely removed. They are provided to demonstrate
   common patterns and best practices, but you can delete them and start fresh.
2. All data returned from tools must be JSON-serializable. Use str for any complex types
   (e.g., convert datetime to ISO string, convert custom objects to string representations).

A Truffle app is a collection of Python functions that your Agent can use as tools.
Each tool is just a regular Python function enhanced with:

1. Type hints for inputs/outputs
2. A @truffle.tool decorator for description and configuration
3. Optional @truffle.args for parameter descriptions
4. Access to context, external APIs, and state management

This template demonstrates three common patterns:
- Context-aware processing (smart_process)
- OpenAI API integration (generate_completion)
- State management (stateful_process)

NOTE: Truffle Apps run in their own isolated execution container, so any secrets exposed here are safe.
"""

import truffle
from typing import Dict, Any, List  # Type hints are required for all tools
from openai import OpenAI  # Truffle will handle installation
from datetime import datetime

@truffle.app(
{description_line}
)
class {class_name}:  # Change class name to match your app's name
    def __init__(self):
        # State persists between tool calls in the same session
        # Use this to store API keys, cache results, or track usage
        self.call_history: List[str] = []
        # Initialize OpenAI client (API key should be set in environment: OPENAI_API_KEY)
        self.client = OpenAI()
    
    def check_api_health(self) -> bool:
        """
        Predicates are optional methods that control when a tool is available.
        Return True if the tool should be available, False otherwise.
        Common uses: rate limiting, time windows, resource checks
        """
        # Simple rate limit: 100 calls per session
        return len(self.call_history) < 100

    @truffle.tool(  # Required decorator for all tools
        description="Process text with length based on context",
        icon="text.word.spacing"  # SF Symbols name for tool icon
    )
    def smart_process(self, text: str, context_tokens: int) -> Dict[str, Any]:
        """
        Tools can access the current context size to adapt their behavior.
        This pattern is useful for:
        - Managing token limits
        - Adjusting output verbosity
        - Optimizing response formats
        """
        self.call_history.append(datetime.now().isoformat())  # Convert datetime to string
        
        # Adapt behavior based on context size
        if context_tokens > 64000:
            summary = text[:100] + "..."
            detail_level = "brief"
        else:
            summary = text[:500] + "..."
            detail_level = "detailed"
            
        # Tools must return a Dict[str, Any] with JSON-serializable values
        return {{
            "processed_text": summary,
            "detail_level": detail_level,
            "context_size": str(context_tokens)  # Convert numbers to strings when needed
        }}

    @truffle.tool(
        description="Generate text using OpenAI's API",
        icon="brain",
        predicates=[check_api_health]  # Optional list of predicates
    )
    @truffle.args(
        prompt="The prompt to send to OpenAI",
        max_tokens="Maximum tokens in the response (default: 150)",
        temperature="Creativity of the response (0-1, default: 0.7)"
    )
    def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        # Track API call - convert datetime to ISO string for JSON serialization
        self.call_history.append(datetime.now().isoformat())
        
        # Make API call
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {{"role": "system", "content": "You are a helpful assistant."}},
                {{"role": "user", "content": prompt}}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Return JSON-serializable values
        return {{
            "text": response.choices[0].message.content,
            "total_tokens": str(response.usage.total_tokens),
            "calls_made": str(len(self.call_history))
        }}

    @truffle.tool(
        description="Process data with state management",
        icon="arrow.triangle.2.circlepath"
    )
    def stateful_process(self, data: str) -> Dict[str, Any]:
        """
        State management allows tools to:
        - Track usage across calls
        - Maintain preferences
        - Share data between tools
        
        Remember: All returned values must be JSON-serializable
        """
        timestamp = datetime.now().isoformat()  # Convert datetime to string
        self.call_history.append(timestamp)
        
        return {{
            "processed": f"Processed {{data}} at {{timestamp}}",
            "total_calls": str(len(self.call_history)),
            "recent_calls": self.call_history[-5:]  # List of strings is JSON-serializable
        }}

# Every Truffle app needs this to run
if __name__ == "__main__":
    truffle.run({class_name}())
''' 