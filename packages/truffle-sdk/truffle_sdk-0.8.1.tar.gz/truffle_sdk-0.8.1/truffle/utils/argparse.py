"""
Custom ArgumentParser that uses Truffle's logging system for custom error messages.
"""

import argparse
from typing import Optional, Any
from .logger import log
from .help import HelpMenu

class TruffleArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that uses Truffle's logging system for error messages."""
    
    def error(self, message: str) -> None:
        """Override the default error method to use Truffle's logging system."""
        log.error(message)
        # Use HelpMenu with show_banner=False to avoid duplicate banners
        HelpMenu(show_banner=False).show_help()
        raise SystemExit(2)
    
    def _print_message(self, message: str, file: Optional[Any] = None) -> None:
        """Override the default message printing to use Truffle's logging system."""
        if message:
            log.detail(message)
    
    def exit(self, status: int = 0, message: Optional[str] = None) -> None:
        """Override the default exit method to use Truffle's logging system."""
        if message:
            log.error(message)
        raise SystemExit(status) 