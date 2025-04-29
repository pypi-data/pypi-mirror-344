"""
CLI Help Menu System

This module manages the display of help information in the Truffle CLI:
- Beautiful command documentation
- Consistent styling with logger
- Clear examples and options
"""

from .logger import log, Colors
from .formatter import Formatter
from .banner import get_truffle_banner, should_show_banner
import sys

class HelpMenu:
    """Manages help menu display and formatting."""
    
    def __init__(self, show_banner=True):
        """Initialize help menu."""
        # Only show banner if explicitly requested AND should_show_banner() is True
        self.show_banner = show_banner and should_show_banner()
        
        self.fmt = Formatter()
        
        # Following Dylan's advice, to avoid problems with f-strings and python versions < 3.12
        # https://stackoverflow.com/questions/78388333/nested-quotes-in-f-string-with-python-3-12-vs-older-versions
        self.indent = "    "
    
    def show_help(self):
        """Display the main help menu."""
        # Banner is already shown in _init, so we don't need to show it again here
        
        # Commands section
        log.main("Commands:")
        
        # Init command
        log.detail(self.fmt.command_box("init [name]", "Create a new app"))
        log.detail("  Options:")
        log.detail(self.indent + self.fmt.option('-n, --name TEXT', 'Name of your app'))
        log.detail(self.indent + self.fmt.option('-d, --description TEXT', 'What your app does'))
        log.detail(self.indent + self.fmt.option('-p, --path PATH', 'Where to create your app'))
        log.detail("  Examples:")
        log.detail(self.indent + self.fmt.example('truffle init', 'Create app interactively'))
        log.detail(self.indent + self.fmt.example('truffle init -n my-app', 'Create app with name'))
        log.detail(self.indent + self.fmt.example('truffle init -p ./apps/hello', 'Create in specific directory'))
        log.detail(self.indent + self.fmt.example('truffle init -n hello -d "Hello World"', 'Create with name and description'))
        
        # Build command
        log.detail(self.fmt.command_box("build [path]", "Build your app"))
        log.detail("  Examples:") 
        log.detail(self.indent + self.fmt.example('truffle build', 'Build app in current directory'))
        log.detail(self.indent + self.fmt.example('truffle build ./my-app', 'Build app in specific directory'))
        
        # Upload command
        log.detail(self.fmt.command_box("upload [path]", "Share your app"))
        log.detail("  Options:")
        log.detail(self.indent + self.fmt.option('LOG_LEVEL=1', 'Default logging (high-level status)'))
        log.detail(self.indent + self.fmt.option('LOG_LEVEL=2', 'Include SSE message content'))
        log.detail(self.indent + self.fmt.option('LOG_LEVEL=3', 'Include raw network data'))
        log.detail("  Examples:")
        log.detail(self.indent + self.fmt.example('truffle upload', 'Upload app in current directory'))
        log.detail(self.indent + self.fmt.example('LOG_LEVEL=2 truffle upload', 'Upload app with SSE message logging'))
        log.detail(self.indent + self.fmt.example('LOG_LEVEL=3 truffle upload ./my-app', 'Upload app with full debug output'))
        
        # Help command
        log.detail(self.fmt.command_box("--help", "Show this help message")) 