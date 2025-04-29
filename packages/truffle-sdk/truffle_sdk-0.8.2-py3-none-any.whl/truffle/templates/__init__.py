"""
Truffle Templates Module

Contains all templates for project initialization and documentation.
Templates are organized by type and purpose.
"""

import uuid
from typing import Dict, Any

from .app import get_main_template
from .docs import get_readme_template, get_llm_xml_template

def get_manifest_template(name: str, description: str) -> Dict[str, Any]:
    """
    Get the template for manifest.json
    
    Args:
        name: Name of the app
        description: Description of the app
        
    Returns:
        Dictionary containing manifest data
    """
    return {
        "name": name,
        "description": description,
        "app_bundle_id": str(uuid.uuid4()),  # Generate a UUID
        "manifest_version": 1,  # Use an integer instead of a string
        "example_prompts": []
    }

def get_requirements_template() -> str:
    """
    Get the template for requirements.txt
    
    Returns:
        String containing default requirements
    """
    return '''# Core dependencies
openai>=1.0.0
requests>=2.31.0

# Add any additional dependencies your app needs below
'''

__all__ = [
    'get_main_template',
    'get_readme_template',
    'get_llm_xml_template',
    'get_manifest_template',
    'get_requirements_template'
] 