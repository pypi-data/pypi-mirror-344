"""Utility functions for inferring application metadata from source code."""

import ast
from pathlib import Path
from typing import Optional, Dict
from .logger import log # Use relative import within utils

def infer_app_info(main_py_path: Path) -> Optional[Dict[str, Optional[str]]]:
    """Parse main.py using AST to find the @truffle.app class and its metadata."""
    if not main_py_path.is_file():
        log.warning(f"Cannot infer app info: {main_py_path} not found.")
        return None
        
    try:
        with open(main_py_path, 'r') as f:
            tree = ast.parse(f.read(), filename=str(main_py_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    # Check if decorator is @truffle.app (covers Name and Attribute access)
                    is_truffle_app = False
                    decorator_call_node = None # Store the call node to extract args

                    # Case 1: @truffle.app(...)
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                        if isinstance(decorator.func.value, ast.Name) and decorator.func.value.id == 'truffle' and decorator.func.attr == 'app':
                            is_truffle_app = True
                            decorator_call_node = decorator
                    # Case 2: from truffle import app; @app(...)
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                         if decorator.func.id == 'app': 
                             log.warning("Found decorator named 'app', assuming it's 'truffle.app'. Consider using '@truffle.app' for clarity.")
                             is_truffle_app = True
                             decorator_call_node = decorator
                    
                    if is_truffle_app and decorator_call_node:
                        class_name = node.name
                        description = None
                        # Extract description from decorator arguments
                        for kw in decorator_call_node.keywords:
                            if kw.arg == 'description' and isinstance(kw.value, ast.Constant):
                                description = kw.value.value # Returns the actual string value
                                break # Found description keyword
                        
                        log.debug(f"Found @truffle.app on class '{class_name}' with description: '{description}'")
                        return {"name": class_name, "description": description}
                        
        log.detail("No class decorated with @truffle.app found in src/app/main.py.")
        return None # No @truffle.app decorator found

    except Exception as e:
        log.error(f"Failed to parse {main_py_path.name} to infer app info: {e}")
        return None # Return None on parsing error

def format_class_name(class_name: str) -> str:
    """Convert class name to snake case if it contains spaces, otherwise leave as is."""
    # If already camelCase (no spaces), return as is
    if " " not in class_name:
        return class_name
        
    # Simple space removal and capitalize each word
    return "".join(word.capitalize() for word in class_name.split()) 