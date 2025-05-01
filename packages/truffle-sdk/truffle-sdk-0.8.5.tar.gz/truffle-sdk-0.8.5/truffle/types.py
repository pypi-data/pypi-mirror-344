"""Type definitions for Truffle SDK"""

## This really should be more robust (Something for if you dont have shit to do)

import os
import shutil
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class TruffleFile:
    """Represents a Truffle file in the filesystem"""
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name


class TruffleImage:
    """Represents a Truffle image in the filesystem"""
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name


@dataclass
class UploadProgress:
    """Progress information for uploads"""
    step: Any
    progress: float
    message: str
    error: Optional[str] = None
    substep: Optional[str] = None
    type: Optional[Any] = None


@dataclass
class UploadError:
    """Error information for upload failures"""
    code: str
    message: str
    details: Optional[str] = None


@dataclass
class UploadState:
    """Current state of an upload"""
    step: Any
    progress: float
    message: str
    error: Optional[UploadError] = None
    logs: List[str] = None
    
    def __post_init__(self):
        if self.logs is None:
            self.logs = []

