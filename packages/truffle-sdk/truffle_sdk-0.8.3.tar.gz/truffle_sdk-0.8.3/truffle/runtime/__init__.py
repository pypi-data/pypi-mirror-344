"""
Runtime module for the Truffle SDK.

This module provides the runtime environment for Truffle applications.
"""

from typing import Optional, Type, Callable
import os
import typing

# Import decorators
from .decorators import (
    tool_decorator as tool,
    args_decorator as args,
    group_decorator as group
)

# Import types
from .types import *

# Import runtime determination
from .determine_runtime import determine_runtime, RuntimeType

# Determine runtime type
RUNTIME_TYPE = determine_runtime()

# Set host based on runtime type
HOST = "localhost:50051" if RUNTIME_TYPE is RuntimeType.CLIENT else None

# Runtime factory function - using lazy import to avoid circular dependency
def Runtime():
    """Get the appropriate runtime class."""
    from .proprietary import TruffleRuntime
    return TruffleRuntime

__all__ = [
    "Runtime", 
    "tool", 
    "args", 
    "group", 
    "HOST",
    "RUNTIME_TYPE",
    "RuntimeType"
]
    
