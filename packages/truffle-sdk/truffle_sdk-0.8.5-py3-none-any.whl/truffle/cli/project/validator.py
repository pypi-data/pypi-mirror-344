"""Project validator module

This module provides a centralized way to validate Truffle projects.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import filecmp

from ...utils.image import validate_png, is_whitelisted_icon

class ProjectValidator:
    """Validates Truffle project structure and content"""
    
    def __init__(self):
        """Initialize the validator"""
        pass
    
    def is_project_directory(self, path: Path) -> bool:
        """Check if path is a valid project directory
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is a valid project directory
        """
        required_files = [
            path / "src" / "app" / "main.py",
            path / "src" / "config" / "manifest.json",
            path / "src" / "config" / "requirements.txt",
            path / "src" / "config" / "icon.png",
            path / "src" / "config" / "llm.xml",
            path / "README.md"
        ]
        return all(f.exists() for f in required_files)
    
    def validate_requirements(self, path: Path) -> Tuple[bool, Optional[str]]:
        """Validate requirements.txt doesn't contain forbidden packages
        
        Args:
            path: Path to the project directory
            
        Returns:
            Tuple[bool, str]: Success status and error message if failed
        """
        requirements_path = path / "src" / "config" / "requirements.txt"
        
        FORBIDDEN_PACKAGES = {
            'truffle-sdk': 'SDK is pre-bundled in the container',
            'grpcio': 'gRPC is pre-bundled with the SDK',
            'protobuf': 'Protobuf is pre-bundled with the SDK'
        }
        
        try:
            with open(requirements_path) as f:
                requirements = f.read().splitlines()
                
            for req in requirements:
                req = req.strip().lower()
                if not req or req.startswith('#'):
                    continue
                    
                package = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if package in FORBIDDEN_PACKAGES:
                    return False, f"Invalid requirement '{package}': {FORBIDDEN_PACKAGES[package]}"
                    
            return True, None
            
        except Exception as e:
            return False, f"Failed to validate requirements: {str(e)}"
    
    def validate_project(self, path: Path) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """Validate project structure and manifest
        
        Args:
            path: Path to the project directory
            
        Returns:
            Tuple[bool, Optional[str], Optional[Dict]]: 
                - Success status
                - Error message if validation failed
                - Manifest data if validation succeeded
        """
        # Check if it's a project directory using the updated list of required files
        if not self.is_project_directory(path):
            # Rebuild the missing list based on the actual required files
            missing = []
            required_map = {
                "src/app/main.py": path / "src" / "app" / "main.py",
                "src/config/manifest.json": path / "src" / "config" / "manifest.json",
                "src/config/requirements.txt": path / "src" / "config" / "requirements.txt",
                "src/config/icon.png": path / "src" / "config" / "icon.png",
                "src/config/llm.xml": path / "src" / "config" / "llm.xml",
                "README.md": path / "README.md"
            }
            for name, file_path in required_map.items():
                if not file_path.exists():
                    missing.append(name)
            
            return False, f"Not a valid Truffle project directory (missing: {', '.join(missing)})", None
        
        # Validate manifest
        try:
            manifest_path = path / "src" / "config" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            
            # Check required fields
            if 'name' not in manifest:
                return False, "Invalid manifest.json (missing 'name' field)", None
            
            # Validate app_bundle_id is a UUID
            if 'app_bundle_id' not in manifest:
                return False, "Invalid manifest.json (missing 'app_bundle_id' field)", None
            
            import uuid
            try:
                uuid.UUID(manifest['app_bundle_id'])
            except (ValueError, TypeError):
                return False, "Invalid manifest.json ('app_bundle_id' must be a UUID)", None
            
            # Validate manifest_version is an integer
            if 'manifest_version' not in manifest:
                return False, "Invalid manifest.json (missing 'manifest_version' field)", None
            
            if not isinstance(manifest['manifest_version'], int):
                return False, "Invalid manifest.json ('manifest_version' must be an integer)", None
                
            # Validate icon.png if it exists
            # Note: is_project_directory should ensure it exists, but double check path here
            icon_path = path / "src" / "config" / "icon.png" # Corrected path
            if icon_path.exists():
                # Check if this is our standard icon
                if is_whitelisted_icon(icon_path):
                    return True, None, manifest
                    
                # If not the standard icon, validate dimensions
                is_valid, error_msg, _ = validate_png(
                    icon_path,
                    min_width=128,  # Minimum size for icons
                    min_height=128,
                    max_width=5000,
                    max_height=5000,
                    require_transparency=False  # Encouraged but not required
                )
                if not is_valid:
                    return False, error_msg, None
                
            return True, None, manifest
            
        except json.JSONDecodeError:
            return False, "Invalid manifest.json format", None
        except Exception as e:
            return False, str(e), None
    
    def get_manifest(self, path: Path) -> Dict:
        """Get the project manifest
        
        Args:
            path: Path to the project directory
            
        Returns:
            Dict: The project manifest
            
        Raises:
            ValueError: If the project is invalid
        """
        success, error, manifest = self.validate_project(path)
        if not success:
            raise ValueError(error)
        return manifest 