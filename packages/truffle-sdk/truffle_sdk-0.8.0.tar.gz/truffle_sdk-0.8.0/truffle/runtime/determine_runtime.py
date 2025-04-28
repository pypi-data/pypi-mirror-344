"""Runtime determination logic."""

import os
from enum import Enum

class RuntimeType(Enum):
    """Runtime type enumeration."""
    CLIENT = 1  # Running as a client
    TRUFFLE = 2 # Running within Truffle

def determine_runtime() -> RuntimeType:
    """Determine which runtime to use based on environment."""
    # Check for Truffle environment variables
    if os.getenv("TRUFFLE_APP_SOCKET") or os.getenv("TRUFFLE_SDK_SOCKET"):
        return RuntimeType.TRUFFLE
    return RuntimeType.CLIENT

