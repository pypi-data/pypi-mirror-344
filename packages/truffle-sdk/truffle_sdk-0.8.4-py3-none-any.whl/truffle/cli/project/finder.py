"""Project finder module"""

from pathlib import Path
from typing import List, Optional

from .validator import ProjectValidator

class ProjectFinder:
    """Handles finding Truffle projects"""
    
    def __init__(self):
        """Initialize the project finder"""
        self.validator = ProjectValidator()
    
    def is_project_dir(self, path: Path) -> bool:
        """Check if path is a valid project directory
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is a valid project directory
        """
        return self.validator.is_project_directory(path)
    
    def find_projects(self, start_path: Path, max_depth: int = 3) -> List[Path]:
        """Find all Truffle projects in the given directory
        
        Args:
            start_path: Path to start searching from
            max_depth: Maximum depth to search
            
        Returns:
            List[Path]: List of paths to Truffle projects
        """
        projects = []
        
        # Check if the start path is a project
        if self.is_project_dir(start_path):
            projects.append(start_path)
        
        # If we've reached max depth, stop
        if max_depth <= 0:
            return projects
        
        # Search subdirectories
        try:
            for item in start_path.iterdir():
                if item.is_dir():
                    projects.extend(self.find_projects(item, max_depth - 1))
        except PermissionError:
            # Skip directories we don't have permission to access
            pass
        
        return projects 