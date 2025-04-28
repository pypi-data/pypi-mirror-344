"""Upload command implementation with real-time progress tracking"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Optional
from ...utils.logger import log
from ...utils.interactive import InteractiveSelector
from ...utils.upload import Uploader
from ..project.finder import ProjectFinder
from ..project.validator import ProjectValidator
from ...runtime.upload.stream import StreamManager
from ...types import UploadProgress

class UploadCommand:
    """Handles uploading Truffle projects with real-time progress tracking"""
    
    def __init__(self, test_mode: bool = False):
        """Initialize the upload command
        
        Args:
            test_mode: Whether to run in test mode
        """
        self.finder = ProjectFinder()
        self.validator = ProjectValidator()
        self.uploader = Uploader()
        self.test_mode = test_mode

    def execute(self, path: Optional[str] = None) -> None:
        """Execute the upload command
        
        Args:
            path: Path to the project directory
        """
        try:
            # Get the project path
            project_path = Path(path) if path else Path.cwd()
            
            # Check if it's a project directory
            if not self.validator.is_project_directory(project_path):
                log.error(f"Not a valid Truffle project directory: {project_path}")
                if not self.test_mode:
                    sys.exit(1)
                return
            
            # Upload the project
            self._upload_project(project_path)
            
        except Exception as e:
            log.error("Upload failed")
            log.detail(str(e))
            if not self.test_mode:
                sys.exit(1)
            return

    def _upload_project(self, path: Path) -> None:
        """Upload a project
        
        Args:
            path: Path to the project directory
        """
        try:
            # Validate the project
            manifest = self.validator.get_manifest(path)
            
            # Create the bundle
            bundle_path = path / f"{manifest['name']}.truffle"
            if not self._create_bundle(path, bundle_path):
                raise ValueError("Failed to create bundle")
            
            # Upload the bundle
            log.info(f"Uploading {manifest['name']}...")
            success, error = self.uploader.upload_file(bundle_path)
            
            if not success:
                raise ValueError(f"Upload failed: {error}")
            
            log.success(f"Uploaded {manifest['name']}")
            
            # Clean up the bundle file
            try:
                if bundle_path.exists():
                    bundle_path.unlink()
                    log.detail(f"Cleaned up bundle file: {bundle_path}")
            except Exception as e:
                log.warning(f"Failed to clean up bundle file: {e}")
            
        except Exception as e:
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
            uploader = Uploader()
            success, error = uploader.create_zip_bundle(src_dir, dst_file)
            
            if not success:
                log.error(f"Failed to create bundle: {error}")
                return False
                
            return True
        except Exception as e:
            log.error(f"Failed to create bundle: {str(e)}")
            return False