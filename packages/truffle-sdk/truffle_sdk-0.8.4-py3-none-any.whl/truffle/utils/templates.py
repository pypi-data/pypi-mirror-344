"""
Project Structure Utility

This module handles the creation of new Truffle project structures.
It manages directory creation, file generation, and icon handling.
"""

import json
import shutil
from pathlib import Path
from typing import Optional

from ..templates import (
    get_main_template,
    get_manifest_template,
    get_requirements_template,
    get_readme_template,
    get_llm_xml_template
)
from .image import get_standard_icon_path
from .logger import log

class ProjectStructure:
    """Handles creation and validation of Truffle project structure"""
    
    def __init__(self, name: str, root_path: Path, description: str = ""):
        """
        Initialize project structure handler
        
        Args:
            name: Name of the project
            root_path: Root path where project will be created
            description: Optional project description
        """
        self.name = name
        self.root_path = Path(root_path)
        self.description = description
        
        # Define standard paths
        self.src_path = self.root_path / "src"
        self.app_path = self.src_path / "app"
        self.config_path = self.src_path / "config"
        
    def create(self) -> None:
        """Create the full project structure"""
        self._create_directories()
        self._create_app_files()
        self._create_config_files()
        self._create_docs()
        self._copy_icon()
        
    def _create_directories(self) -> None:
        """Create project directory structure"""
        # Create directories if they don't exist
        self.root_path.mkdir(parents=True, exist_ok=True)
        self.src_path.mkdir(exist_ok=True)
        self.app_path.mkdir(exist_ok=True)
        self.config_path.mkdir(exist_ok=True)
        
        log.created_file(str(self.root_path))
        
    def _create_app_files(self) -> None:
        """Create application source files"""
        # Create main.py
        main_path = self.app_path / "main.py"
        main_path.write_text(get_main_template(self.name))
        log.created_file("main.py")
            
    def _create_config_files(self) -> None:
        """Create configuration files"""
        # Create manifest.json
        manifest_path = self.config_path / "manifest.json"
        manifest_content = get_manifest_template(self.name, self.description)
        manifest_path.write_text(json.dumps(manifest_content, indent=2))
        log.created_file("manifest.json")
        
        # Create requirements.txt
        requirements_path = self.config_path / "requirements.txt"
        requirements_path.write_text(get_requirements_template())
        log.created_file("requirements.txt")
        
    def _create_docs(self) -> None:
        """Create documentation files"""
        # Create README.md
        readme_path = self.root_path / "README.md"
        readme_path.write_text(get_readme_template(self.name, self.description))
        log.created_file("README.md")
        
        # Create LLM.xml
        llm_path = self.config_path / "llm.xml"
        llm_path.write_text(get_llm_xml_template(self.name, self.description))
        log.created_file("llm.xml")
        
    def _copy_icon(self) -> None:
        """Copy default icon to project"""
        icon_source = get_standard_icon_path()
        icon_dest = self.root_path / "icon.png"
        shutil.copy2(icon_source, icon_dest)
        log.created_file("icon.png")
        
    def validate(self) -> bool:
        """
        Validate project structure
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check required directories exist
            for path in [self.root_path, self.src_path, self.app_path, self.config_path]:
                if not path.is_dir():
                    return False
                    
            # Check required files exist
            required_files = [
                self.app_path / "main.py",
                self.config_path / "manifest.json",
                self.config_path / "requirements.txt",
                self.root_path / "README.md",
                self.config_path / "llm.xml",
                self.root_path / "icon.png"
            ]
            
            for file in required_files:
                if not file.is_file():
                    return False
                    
            return True
            
        except Exception:
            return False 