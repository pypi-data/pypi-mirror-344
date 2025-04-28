"""Platform initialization module."""

import os
import sys
from pathlib import Path
from ..runtime.determine_runtime import determine_runtime, RuntimeType

# Socket configuration
if os.getenv("TRUFFLE_APP_SOCKET") is not None:
    APP_SOCK = os.getenv("TRUFFLE_APP_SOCKET")
else:
    APP_SOCK = "unix:///tmp/truffle.sock"

if os.getenv("TRUFFLE_SDK_SOCKET") is not None:
    SDK_SOCK = os.getenv("TRUFFLE_SDK_SOCKET")
else:
    SDK_SOCK = "unix:///tmp/truffle-sdk.sock"

# Shared directory configuration
SHARED_DIR = (
    os.getenv("TRUFFLE_SHARED_DIR")
    if os.getenv("TRUFFLE_SHARED_DIR") is not None
    else "/root/shared"  # container default 1.31.25
)

# Determine runtime type
RUNTIME_TYPE = determine_runtime()

# Validate socket configuration in Truffle mode
if RUNTIME_TYPE is RuntimeType.TRUFFLE:
    if not os.getenv("TRUFFLE_APP_SOCKET") or not os.getenv("TRUFFLE_SDK_SOCKET"):
        raise Exception("TRUFFLE_APP_SOCKET and TRUFFLE_SDK_SOCKET must be set when using Truffle SDK")

# Export configuration
__all__ = ["APP_SOCK", "SDK_SOCK", "SHARED_DIR", "RUNTIME_TYPE"]
        