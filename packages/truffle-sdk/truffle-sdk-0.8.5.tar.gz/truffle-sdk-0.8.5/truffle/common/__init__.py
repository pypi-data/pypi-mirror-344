"""
Common utilities for the Truffle SDK.

This module provides common utilities used throughout the SDK.
"""

import logging
from typing import Optional

from ..utils.logger import log

def get_logger() -> logging.Logger:
    """Get a logger instance for the Truffle SDK.
    
    Returns:
        A logger instance configured for the Truffle SDK.
    """
    return logging.getLogger("truffle")

# Re-export the log instance for convenience
__all__ = ["get_logger", "log"]


