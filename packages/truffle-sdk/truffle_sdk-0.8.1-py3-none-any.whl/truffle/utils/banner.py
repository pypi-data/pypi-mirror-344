"""
Banner System

This module handles the TRUFFLE ASCII art banner and tagline display.
"""

import os
import shutil
from .logger import Colors

def should_show_banner() -> bool:
    """
    Determine if the banner should be shown based on environment.
    Returns False if running in a container/app context (indicated by socket env vars).
    """
    return not (os.getenv("TRUFFLE_APP_SOCKET") or os.getenv("TRUFFLE_SDK_SOCKET"))

def get_truffle_banner() -> str:
    """Create the TRUFFLE ASCII art banner with tagline."""
    # Skip banner in container/app context
    if not should_show_banner():
        return ""
        
    # Get terminal width
    term_width = shutil.get_terminal_size().columns
    
    # Use compact banner for narrow terminals (less than 70 columns)
    if term_width < 70:
        banner = f"""{Colors.MAIN}
  ████████╗██████╗ ██╗   ██╗███████╗███████╗██╗     ███████╗
  ╚══██╔══╝██╔══██╗██║   ██║██╔════╝██╔════╝██║     ██╔════╝
     ██║   ██████╔╝██║   ██║█████╗  █████╗  ██║     █████╗  
     ██║   ██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██║     ██╔══╝  
     ██║   ██║  ██║╚██████╔╝██║     ██║     ███████╗███████╗
     ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚══════╝{Colors.RESET}"""
    else:
        banner = f"""{Colors.MAIN}
  ████████╗██████╗ ██╗   ██╗███████╗███████╗██╗     ███████╗
  ╚══██╔══╝██╔══██╗██║   ██║██╔════╝██╔════╝██║     ██╔════╝
     ██║   ██████╔╝██║   ██║█████╗  █████╗  ██║     █████╗  
     ██║   ██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██║     ██╔══╝  
     ██║   ██║  ██║╚██████╔╝██║     ██║     ███████╗███████╗
     ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚══════╝{Colors.RESET}"""

    # Add tagline centered under banner
    # Using regular font with italic styling for better dark mode rendering
    tagline = "We won't blame you for thinking it's a sex toy."
    
    # Banner starts at column 2 and is 65 characters wide
    banner_start = 2
    banner_width = 65
    # Calculate padding to center tagline under the banner
    # Shift left by 5 spaces to align middle of tagline with middle of banner
    padding = banner_start + (banner_width - len(tagline)) // 2 - 5
    
    # Use whisper color and triple italic escape codes for more dramatic slant
    # Also use \x1B[2m for slightly dimmer text to appear smaller
    centered_tagline = f"\n\n{' ' * padding}{Colors.WHISPER}\x1B[2m\x1B[3m\x1B[3m\x1B[3m{tagline}\x1B[0m{Colors.RESET}\n\n"
    
    return banner + centered_tagline 