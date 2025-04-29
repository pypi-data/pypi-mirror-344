"""Build command implementation"""

import os
import sys
import json
import ast
from pathlib import Path
from typing import Optional
from ...utils.logger import log
from ...utils.interactive import InteractiveSelector
from ...utils.inferparse import infer_app_info, format_class_name
from ..project.finder import ProjectFinder
from ..project.validator import ProjectValidator

class BuildCommand:
    """Handles building Truffle projects"""
    
    def __init__(self):
        self.finder = ProjectFinder()  # handles magic project location
        self.validator = ProjectValidator()

    def execute(self, path: Optional[str] = None) -> None:
        """Build a Truffle project"""
        try:
            # Get the project path
            project_path = Path(path).resolve() if path else Path.cwd().resolve()
            
            # Validate the project directory structure and required files
            if not self.validator.is_project_directory(project_path):
                log.error(f"Directory structure is not a valid Truffle project: {project_path}")
                log.detail("Expected structure: src/app/main.py, src/config/manifest.json, etc.")
                sys.exit(1)
            
            # Build the project
            self._build_project(project_path)
            
        except Exception as e:
            log.error("Build failed")
            log.detail(str(e))
            sys.exit(1)

    def _build_project(self, path: Path) -> None:
        """Core build logic, including manifest loading and potential inference."""
        try:
            # Define key paths
            manifest_path = path / "src" / "config" / "manifest.json"
            main_py_path = path / "src" / "app" / "main.py"

            # Validate requirements first
            success, error = self.validator.validate_requirements(path)
            if not success:
                raise ValueError(f"Requirements validation failed: {error}")
            
            # Load manifest (assuming validator reads from src/config/manifest.json)
            manifest = self.validator.get_manifest(path)
            manifest_updated = False
            app_info = None # Cache inference result

            # --- Determine App Name --- 
            if manifest.get("name") is None:
                log.detail("App name not found in manifest, attempting inference...")
                # Use the utility function
                app_info = infer_app_info(main_py_path)
                if app_info is None or not app_info.get("name"):
                    log.detail("App name was not found in manifest.json and could not be inferred. Using default: 'MyApp'.")
                    final_name = "MyApp"
                    manifest["name"] = final_name
                    log.info(f"Using default app name: {final_name}")
                    manifest_updated = True
                else:
                    # Use the utility function for formatting if name WAS inferred
                    final_name = format_class_name(app_info["name"])
                    manifest["name"] = final_name
                    log.detail(f"Inferred app name: {final_name}")
                    manifest_updated = True
            
            # --- Determine App Description --- 
            if not manifest.get("description"): # Run if description is missing or empty
                log.detail("App description not found or empty in manifest, attempting inference...")
                # Use cached info if name was inferred, otherwise infer now
                if app_info is None:
                    # Use the utility function
                    app_info = infer_app_info(main_py_path)
                
                # Default to standard description if not found or None after inference
                final_desc = app_info.get("description") if app_info else None
                if not final_desc: # Apply default if inferred value is None or ""
                    final_desc = "This is a description" # Use default description
                    log.info(f"Using default app description: '{final_desc}'") # Log using default
                else:
                     log.detail(f"Inferred app description: '{final_desc}'") # Log inferred value

                manifest["description"] = final_desc
                manifest_updated = True

            # --- Persist Manifest Updates (Optional) --- 
            if manifest_updated:
                try:
                    with open(manifest_path, 'w') as f:
                        json.dump(manifest, f, indent=2)
                    log.info(f"Saved inferred configuration to {manifest_path.relative_to(path)}")
                except Exception as e:
                    log.warning(f"Could not write updated manifest back to {manifest_path.relative_to(path)}: {e}")
                    log.detail("Build will proceed with in-memory configuration.")

            # --- Proceed with original build steps using the final manifest data --- 

            # Ensure final name exists before proceeding (should always pass after checks)
            final_app_name = manifest.get("name")
            if not final_app_name:
                 log.error("Internal error: App name is missing after inference/check.")
                 sys.exit(1)
                 
            # Create the bundle using the final name
            bundle_path = path / f"{final_app_name}.truffle"
            if not self._create_bundle(path, bundle_path):
                # _create_bundle logs its own errors
                raise ValueError("Failed to create bundle")
            
            log.success(f"Built '{final_app_name}' successfully.")
            log.detail(f"Bundle created at: {bundle_path.relative_to(path.parent)}") # Show path relative to workspace if possible
            
        except Exception as e:
            # Catch specific errors if needed, otherwise re-raise as ValueError
            raise ValueError(str(e))

    def _create_bundle(self, src_dir: Path, dst_file: Path) -> bool:
        """Create the build bundle
        
        Args:
            src_dir: Source directory
            dst_file: Destination file
            
        Returns:
            bool: True if successful
        """
        try:
            # Use the consolidated create_zip_bundle function
            from ...utils.upload import Uploader
            uploader = Uploader()
            success, error = uploader.create_zip_bundle(src_dir, dst_file)
            
            if not success:
                log.error(f"Failed to create bundle: {error}")
                return False
                
            return True
        except Exception as e:
            log.error(f"Failed to create bundle: {str(e)}")
            return False

    def _is_project_directory(self, path: Path) -> bool:
        """Check if path is valid project directory"""
        required_files = [
            path / "src" / "app" / "main.py",
            path / "src" / "config" / "manifest.json",
            path / "src" / "config" / "requirements.txt",
            path / "src" / "config" / "icon.png"  # Updated path to match validator
        ]
        return all(f.exists() for f in required_files)
