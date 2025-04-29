"""
Documentation templates module.
Contains templates for README and LLM.xml documentation.
"""

def get_readme_template(app_name: str, description: str = "") -> str:
    """
    Get the README template.
    
    Args:
        app_name: Name of the application
        description: Optional description
        
    Returns:
        Formatted README template
    """
    return f'''# {app_name}

{description if description else "A starter template for building Truffle apps with examples of core functionality and best practices."}

## Project Structure

```
{app_name}/
├── README.md           # This documentation
├── src/
│   ├── app/           # Your application code
│   │   ├── main.py    # Main app logic with example tools
│   └── config/        # System configuration
│       ├── manifest.json
│       ├── llm.xml    # LLM documentation
│       └── requirements.txt
```

## Quick Start

1. Review `main.py` for working examples of:
   - Context-aware tools
   - OpenAI API integration
   - State management
   - Predicate usage
   - Don't forget to add any packages used to requirements.txt

## Key Files

- `main.py`: Contains example tools showcasing different Truffle SDK features. This is where you will write your app logic.
- `llm.xml`: App-building document to feed into an LLM
- `manifest.json`: Auto-generated app configuration
- `requirements.txt`: Project dependencies

## Development

Your app code goes in `src/app/main.py`. The template includes examples of:
- Type hints and decorators
- API integration patterns
- State management
- Context-aware processing

## Learn More

- Visit the [Docs](https://docs.itsalltruffles.com) for more resources
'''

def get_llm_xml_template(app_name: str, description: str = "") -> str:
    """
    Get the LLM.xml template.
    
    Args:
        app_name: Name of the application
        description: Optional description
        
    Returns:
        Formatted LLM.xml template
    """
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<truffle-app-guide>
    <overview>
        <purpose>
            This guide helps AI agents assist users in building Truffle apps. Each app consists of Python functions that are transformed into tools for the Truffle Agent to use.
        </purpose>
        <core-concepts>
            <concept name="Tool">A Python function decorated with @truffle.tool that your Agent can use</concept>
            <concept name="App">A collection of related tools bundled together. An app can be either a single tool or multiple related tools grouped in the same class</concept>
            <concept name="Agent">The AI assistant that uses your tools via the Truffle MacOS client</concept>
        </core-concepts>
        <important-implementation-note>
            When implementing a Truffle app, follow these key principles:
            1. REMOVE ALL EXAMPLE FUNCTIONS from main.py unless the user specifically requests that functionality. The examples (smart_process, generate_completion, stateful_process) are provided only as reference implementations.
            2. Keep the implementation SIMPLE and STRAIGHTFORWARD by default. Only use advanced Truffle features (predicates, context-awareness, state management, etc.) if the user explicitly requests a full-featured app.
            3. Start with the minimal code needed to solve the user's problem. Don't add complexity unless specifically asked for.
            4. All data returned from tools MUST be JSON-serializable. Use strings (str) for any complex types or numbers:
               - Convert datetime objects to ISO strings
               - Convert numbers to strings
               - Convert custom objects to string representations
               - Use Dict[str, str] instead of Dict[str, Any] when possible
            5. NEVER add truffle or truffle-sdk to requirements.txt - only add third-party packages your app needs.
        </important-implementation-note>
    </overview>

    <project-structure>
        <directory-layout>
            <root name="{app_name}">
                <file name="README.md">User-facing documentation with project overview</file>
                <directory name="src">
                    <directory name="app">
                        <description>Contains user-editable application code</description>
                        <file name="main.py">Main application code - remove example tools unless specifically needed</file>
                    </directory>
                    <directory name="config">
                        <description>Generated and system configuration files</description>
                        <file name="manifest.json">Auto-generated app configuration</file>
                        <file name="llm.xml">This LLM-friendly documentation</file>
                        <file name="requirements.txt">Project dependencies</file>
                    </directory>
                </directory>
            </root>
        </directory-layout>
        <important-notes>
            <note>All user code should be written in src/app/main.py</note>
            <note>New dependencies must be added to requirements.txt</note>
            <note>manifest.json is auto-generated - do not edit manually</note>
            <note>REMOVE ALL EXAMPLE FUNCTIONS from main.py unless specifically requested by the user</note>
            <note>Keep implementation simple by default - only use advanced features when requested</note>
            <note>NEVER add truffle or truffle-sdk to requirements.txt - only add third-party packages your app needs</note>
        </important-notes>
    </project-structure>

    <interaction-flow>
        <initial-questions>
            <question>What specific task or problem would you like your Truffle app to solve?</question>
            <question>Can you describe the ideal interaction between you and your Agent when using this tool?</question>
            <question>What type of data or resources will your tool need to work with?</question>
            <question>Are there any specific outputs or formats you need from your tool?</question>
            <question>Are there any related functionalities that would make sense to group together in this app?</question>
            <question>Do you need any of the example functionality provided in the template?</question>
            <question>Do you need advanced features like state management, predicates, or context-awareness?</question>
        </initial-questions>
    </interaction-flow>

    <code-template>
        <important-note>
            When designing your app, remember these critical points:
            1. Syntactical correctness is crucial for firmware compatibility. Your code must strictly follow Python type hints, proper return values, and decorator syntax as shown in the template.
            2. Related tools should be grouped together in the same class. For example, if building a research assistant, functions for searching, taking notes, and summarizing could all be tools within a single ResearchApp class.
            3. REMOVE ALL EXAMPLE FUNCTIONS unless the user specifically requests that functionality. The template includes example tools that should be deleted if not explicitly needed.
            4. All values returned from tools must be JSON-serializable. Convert complex types (like datetime) to strings, and ensure all numbers are converted to strings when needed.
            5. Keep the implementation simple and straightforward unless the user specifically requests advanced features. Start with basic functionality and only add complexity when needed.
        </important-note>
        <main-py>
            <structure>
                <imports>
                    import truffle
                    from typing import Dict, Any, List
                    <!-- Do not import str as it is built-in -->
                    # Add any additional imports needed for your specific use case
                    # Remove unused imports from examples
                </imports>
                
                <class-definition>
                    class {app_name}:
                        def __init__(self):
                            # Initialize any state variables needed
                            # State persists between tool calls in the same session
                            # Remove any unused state from examples
                            pass

                        @truffle.tool(
                            description="Clear description of what your tool does",
                            icon="appropriate-sf-symbol-name"
                        )
                        @truffle.args(param="Description of what this parameter does")
                        def your_tool_name(self, param: type) -> Dict[str, Any]:
                            # Your tool's logic here
                            # Remember: All return values must be JSON-serializable
                            return {{"result": "your result"}}

                        # Additional tools should be added as methods in this class
                        # Group related functionality together
                        # Remove all example tools unless specifically requested

                if __name__ == "__main__":
                    truffle.run({app_name}())
                </class-definition>
            </structure>
        </main-py>
    </code-template>

    <api-integration>
        <overview>
            Since Truffle tools are just decorated Python functions, you can easily integrate any API using standard Python requests or API-specific libraries. Each app runs in its own execution container, making it safe to include API keys directly in the code.
        </overview>

        <key-points>
            <point>API keys can be safely hardcoded in main.py as each app runs in an isolated container</point>
            <point>Use standard Python libraries and practices for API calls</point>
            <point>Add any API dependencies to requirements.txt (except truffle/truffle-sdk)</point>
            <point>Error handling is managed by the agent - focus on core functionality</point>
            <point>Remember to convert API responses to JSON-serializable types (usually strings)</point>
            <point>Remove the OpenAI example unless specifically requested by the user</point>
        </key-points>

        <example>
            <code>
                from openai import OpenAI  # Remove if not using OpenAI
                
                class {app_name}:
                    def __init__(self):
                        self.client = OpenAI()  # Remove if not using OpenAI

                    @truffle.tool(
                        description="Generate text using OpenAI",
                        icon="brain"
                    )
                    def generate_text(self, prompt: str) -> Dict[str, str]:  # Note: Dict[str, str] ensures JSON-serializable
                        response = self.client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{{"role": "user", "content": prompt}}]
                        )
                        return {{"text": response.choices[0].message.content}}
                    # Remove this example unless specifically requested by the user
            </code>
        </example>
    </api-integration>

    <code-guidelines>
        <rule>All functions must use type hints for parameters and return values</rule>
        <rule>Every tool must return a Dict[str, Any] with JSON-serializable values</rule>
        <rule>Tool descriptions should be clear and specific</rule>
        <rule>Use appropriate SF Symbols for icons</rule>
        <rule>Include only the code necessary for your specific needs - remove unused examples</rule>
        <rule>Maintain proper Python syntax and best practices</rule>
        <rule>Group related tools within the same app class</rule>
        <rule>Add new dependencies to requirements.txt (NEVER add truffle/truffle-sdk)</rule>
        <rule>Convert complex types to strings before returning</rule>
        <rule>Remove all example functions unless explicitly requested by the user</rule>
        <rule>Keep implementation simple by default - only add advanced features when requested</rule>
    </code-guidelines>

    <best-practices>
        <practice>Keep tools focused on single responsibilities</practice>
        <practice>Use descriptive names for tools and parameters</practice>
        <practice>Add helpful argument descriptions using @truffle.args</practice>
        <practice>Store state in class variables when needed for persistence</practice>
        <practice>Consider grouping complementary tools that work together</practice>
        <practice>Document any special setup or API keys needed</practice>
        <practice>Always ensure return values are JSON-serializable</practice>
        <practice>Remove all example code that isn't specifically requested</practice>
        <practice>Start with simple implementations and only add complexity when needed</practice>
        <practice>Use advanced Truffle features only when explicitly requested</practice>
    </best-practices>

    <deployment-steps>
        <step order="1">
            <instruction>Remove all example functions from main.py unless specifically needed</instruction>
        </step>
        <step order="2">
            <instruction>cd into your project directory: cd {app_name}</instruction>
        </step>
        <step order="3">
            <instruction>Build your app: truffle build</instruction>
            <note>This packages your Python code into a format your Agent can use</note>
        </step>
        <step order="4">
            <instruction>Upload to Truffle: truffle upload</instruction>
            <note>This makes your app available to your Agent</note>
        </step>
        <step order="5">
            <instruction>Return to the Truffle MacOS client to start using your tool</instruction>
        </step>
    </deployment-steps>
</truffle-app-guide>
''' 