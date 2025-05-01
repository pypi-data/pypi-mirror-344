"""Project creator module

This module handles the creation of new Truffle projects.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional
from ...utils.logger import log
from ...utils.templates import get_main_template, get_manifest_template, get_readme_template, get_llm_xml_template, ProjectStructure
from ...utils.image import is_whitelisted_icon, get_standard_icon_path
import uuid

class ProjectCreator:
    """Creates new Truffle projects"""
    
    def create(self, path: str, name_override: Optional[str] = None, description_override: Optional[str] = None) -> Path:
        """Create a new project structure at the specified path.
        
        Handles creation of directories and base files (main.py, requirements.txt, icon.png)
        and creates a manifest.json containing any provided overrides for name/description.
        The final name and description are determined during the build process.

        Args:
            path: The target path where the project structure should be created.
                  This path is confirmed by the caller (e.g., init command).
            name_override: Optional name provided via `-n` flag to override inferred name.
            description_override: Optional description provided via `-d` flag to override decorator description.
            
        Returns:
            Path: Path object representing the created project structure root.
            
        Raises:
            FileExistsError: If the target project directory already exists and is not empty.
            ValueError: If file creation fails.
            FileNotFoundError: If icon copy fails.
        """
        # Path is now provided definitively by the caller
        project_path = Path(path)

        # Check if directory exists (or if it's a file)
        if project_path.exists() and project_path.is_file():
             raise FileExistsError(f"Target path exists and is a file: {project_path}")
        # If it exists as a directory, check if it's empty or contains expected structure
        # For simplicity now, we'll just raise if it exists and isn't empty, 
        # or maybe allow if it only contains e.g. .git? Let's be strict for now.
        if project_path.exists() and any(project_path.iterdir()):
             # Refine this check later if needed to allow init in existing repo etc.
             raise FileExistsError(f"Directory already exists and is not empty: {project_path}")
            
        # Create project directories (including src/app and src/config)
        src_app_path = project_path / "src" / "app"
        src_config_path = project_path / "src" / "config"
        try:
            src_app_path.mkdir(parents=True, exist_ok=True) # Use exist_ok=True since parent (project_path) might exist if cwd
            src_config_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
             raise ValueError(f"Could not create project directories: {e}")

        # Determine placeholder name for templates if override not provided
        # Using a generic name. Build process will infer the real one later.
        initial_template_name = name_override if name_override else "MyTruffleApp"

        # Create individual project files
        # Pass overrides directly to manifest creation
        self._create_manifest(src_config_path, name_override, description_override)
        self._create_requirements(src_config_path)
        self._create_main(src_app_path, initial_template_name, description_override)
        self._create_icon(src_config_path) # Let's put config files together
        # Add calls to create docs
        self._create_readme(project_path, initial_template_name, description_override or "")
        self._create_llm_xml(src_config_path, initial_template_name, description_override or "")
            
        return project_path
        
    def _create_manifest(self, path: Path, name_override: Optional[str], description_override: Optional[str]) -> None:
        """Create manifest.json containing required fields and any explicit overrides.
        
        Generates a new app_bundle_id (UUID) and sets a default manifest_version.
        If name/description are provided via overrides (init flags), they are
        written directly as 'name' and 'description'. 
        If not provided, these keys will be absent, and the build process
        will be responsible for inferring them and potentially updating this file.
        """
        try:
            # Base manifest structure - includes required fields
            manifest_data = {
                "builder_version": "0.1.0", # Example field, define properly
                "app_bundle_id": str(uuid.uuid4()), # Generate and add required UUID
                "manifest_version": 1, # Add required version
                "example_prompts": [] # Add empty list for example prompts
            }
            
            # Add name if override exists
            if name_override is not None:
                manifest_data["name"] = name_override
            
            # Add description if override exists
            if description_override is not None:
                manifest_data["description"] = description_override
                
            manifest_path = path / "manifest.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists
            with open(manifest_path, "w") as f:
                json.dump(manifest_data, f, indent=2)
            log.created_file(str(manifest_path.relative_to(path.parent.parent))) # Show relative path like src/config/manifest.json
        except Exception as e:
            raise ValueError(f"Could not create manifest.json: {e}")
            
    def _create_requirements(self, path: Path) -> None:
        """Create requirements.txt with necessary dependencies"""
        try:
            reqs_path = path / "requirements.txt"
            requirements = [
                "requests>=2.31.0",  # For HTTP requests
            ]
            reqs_path.write_text("\n".join(requirements))
            log.created_file("requirements.txt")
        except Exception as e:
            raise ValueError(f"Could not create requirements.txt: {e}")
            
    def _create_main(self, path: Path, name: str, description_override: Optional[str] = None) -> None:
        """Create main.py with rich template using a placeholder name and optional description."""
        try:
            main_path = path / "main.py"
            template = get_main_template(name, description_override)
            main_path.write_text(template)
            log.created_file(str(main_path.relative_to(path.parent.parent))) # Show relative path like src/app/main.py
        except Exception as e:
            raise ValueError(f"Could not create main.py: {e}")
            
    def _create_icon(self, path: Path) -> None:
        """Create icon.png using the Truffle icon in the specified path (e.g., src/config)."""
        icon_path = path / "icon.png"
        truffle_icon_path = get_standard_icon_path()
        
        if not truffle_icon_path.exists():
            raise FileNotFoundError(f"Could not find Truffle icon at: {truffle_icon_path}")
            
        try:
            shutil.copy2(truffle_icon_path, icon_path)
            # Verify the copy was successful by checking if it's whitelisted
            if not is_whitelisted_icon(icon_path):
                raise FileNotFoundError("Copied icon does not match standard Truffle icon")
            log.created_file(str(icon_path.relative_to(path.parent.parent))) # Show relative path like src/config/icon.png
        except Exception as e:
            raise FileNotFoundError(f"Failed to copy Truffle icon: {str(e)}")

    def _create_readme(self, path: Path, name: str, description: str) -> None:
        """Create README.md in the project root."""
        try:
            readme_path = path / "README.md"
            template = get_readme_template(name, description)
            readme_path.write_text(template)
            # Log relative to CWD if possible, else just filename
            try:
                log_path = readme_path.relative_to(Path.cwd())
            except ValueError:
                log_path = readme_path.name
            log.created_file(str(log_path))
        except Exception as e:
            raise ValueError(f"Could not create README.md: {e}")

    def _create_llm_xml(self, path: Path, name: str, description: str) -> None:
        """Create llm.xml in the specified path (e.g., src/config)."""
        try:
            llm_path = path / "llm.xml"
            template = get_llm_xml_template(name, description)
            llm_path.write_text(template)
            log.created_file(str(llm_path.relative_to(path.parent.parent))) # Show relative path like src/config/llm.xml
        except Exception as e:
            raise ValueError(f"Could not create llm.xml: {e}") 