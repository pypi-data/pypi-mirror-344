"""
CLI Formatting System

This module provides beautiful formatting utilities for the Truffle CLI:
- Command boxes and containers
- Example and option formatting
- Consistent styling with the logger
"""

import shutil
import sys
from .logger import Colors, Symbols

class Formatter:
    """Beautiful CLI formatting for help menus and general output."""
    
    @staticmethod
    def command_box(command: str, description: str = "") -> str:
        """Create a small container for a command."""
        # Calculate width based on longest line
        width = max(
            len(command) + 4,  # Command width + padding
            len(description) + 4 if description else 0,  # Description width + padding
            30  # Minimum width
        )
        
        # Create box with rounded corners
        top = f"{Colors.MAIN}╭{'─' * (width-2)}╮{Colors.RESET}"
        bottom = f"{Colors.MAIN}╰{'─' * (width-2)}╯{Colors.RESET}"
        
        # Left align the command and description with consistent dark theme
        cmd_line = f"{Colors.MAIN}│{Colors.RESET} {Colors.MAIN}{command.ljust(width-4)}{Colors.RESET}{Colors.MAIN} │{Colors.RESET}"
        if description:
            desc_line = f"{Colors.MAIN}│{Colors.RESET} {Colors.DIM_GRAY}{description.ljust(width-4)}{Colors.RESET}{Colors.MAIN} │{Colors.RESET}"
            return f"{top}\n{cmd_line}\n{desc_line}\n{bottom}"
        return f"{top}\n{cmd_line}\n{bottom}"

    @staticmethod
    def example(command: str, description: str = "") -> str:
        """Format a command example."""
        return f"{Colors.MAIN}{Symbols.ARROW} {command}{Colors.RESET}  {Colors.LIGHT_GRAY}{description}{Colors.RESET}"

    @staticmethod
    def option(name: str, description: str = "") -> str:
        """Format a command option."""
        return f"{Colors.DIM_GRAY}{name}{Colors.RESET}  {Colors.LIGHT_GRAY}{description}{Colors.RESET}" 