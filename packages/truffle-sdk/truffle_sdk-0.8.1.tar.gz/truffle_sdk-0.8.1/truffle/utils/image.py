"""Image validation utilities

This module provides utilities for validating image files, particularly PNG icons.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import filecmp

from .errors import ErrorHandler, ErrorCode, ErrorContext, ValidationError
from .logger import log

def get_png_dimensions(file_path: Path) -> Tuple[int, int]:
    """Get the dimensions of a PNG file by reading its header.
    
    Args:
        file_path: Path to the PNG file
        
    Returns:
        Tuple[int, int]: Width and height of the image
        
    Raises:
        ValueError: If the file is not a valid PNG or has invalid structure
    """
    with open(file_path, "rb") as f:
        signature = f.read(8)  
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("Not a valid PNG file: " + str(file_path))
        f.read(4) 
        if f.read(4) != b"IHDR":
            raise ValueError("Invalid PNG structure: header not found in " + str(file_path))

        width = int.from_bytes(f.read(4), "big")
        height = int.from_bytes(f.read(4), "big")
        return width, height

def validate_png(
    file_path: Path, 
    min_width: int = 128, 
    min_height: int = 128, 
    max_width: int = 5000, 
    max_height: int = 5000,
    require_transparency: bool = False
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Validate a PNG file meets size and format requirements.
    
    Args:
        file_path: Path to the PNG file
        min_width: Minimum width in pixels
        min_height: Minimum height in pixels
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        require_transparency: Whether to require transparency (not supported in simple validator)
        
    Returns:
        Tuple[bool, Optional[str], Optional[Dict[str, Any]]]: 
            - Success status
            - Error message if validation failed
            - Image metadata if validation succeeded
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            context = ErrorContext(
                source="utils.image",
                operation="validate_png",
                details={"file_path": str(file_path)}
            )
            error = ErrorHandler.create_error(
                ErrorCode.FILE_NOT_FOUND,
                f"Icon file not found: {file_path}",
                context=context
            )
            return False, str(error), None
            
        # Get dimensions using the simple validator
        try:
            width, height = get_png_dimensions(file_path)
        except ValueError as e:
            context = ErrorContext(
                source="utils.image",
                operation="validate_png",
                details={"file_path": str(file_path)}
            )
            error = ErrorHandler.create_error(
                ErrorCode.INVALID_FILE_FORMAT,
                str(e),
                context=context
            )
            return False, str(error), None
            
        # Check dimensions
        if width < min_width or height < min_height:
            context = ErrorContext(
                source="utils.image",
                operation="validate_png",
                details={
                    "file_path": str(file_path),
                    "width": width,
                    "height": height,
                    "min_width": min_width,
                    "min_height": min_height
                }
            )
            error = ErrorHandler.create_error(
                ErrorCode.VALIDATION_ERROR,
                f"Icon dimensions too small: {width}x{height}. Minimum: {min_width}x{min_height}",
                context=context
            )
            return False, str(error), None
            
        if width > max_width or height > max_height:
            context = ErrorContext(
                source="utils.image",
                operation="validate_png",
                details={
                    "file_path": str(file_path),
                    "width": width,
                    "height": height,
                    "max_width": max_width,
                    "max_height": max_height
                }
            )
            error = ErrorHandler.create_error(
                ErrorCode.VALIDATION_ERROR,
                f"Icon dimensions too large: {width}x{height}. Maximum: {max_width}x{max_height}",
                context=context
            )
            return False, str(error), None
            
        # Note: Transparency check removed as it's not supported in simple validator
            
        # Return success with metadata
        metadata = {
            "width": width,
            "height": height,
            "format": "PNG"
        }
        
        return True, None, metadata
            
    except Exception as e:
        context = ErrorContext(
            source="utils.image",
            operation="validate_png",
            details={"file_path": str(file_path)},
            stack_trace=str(e)
        )
        error = ErrorHandler.create_error(
            ErrorCode.FILE_READ_ERROR,
            f"Error validating PNG: {str(e)}",
            context=context,
            original_error=e
        )
        return False, str(error), None 

def get_standard_icon_path() -> Path:
    """Get the path to the standard Truffle icon.
    
    Returns:
        Path: Path to the standard icon
    """
    return Path(__file__).parent.parent / "icons" / "truffle_icon.png"

def is_whitelisted_icon(icon_path: Path) -> bool:
    """
    Check if an icon is the standard Truffle icon.
    
    Args:
        icon_path: Path to the icon file to check
        
    Returns:
        bool: True if the icon matches the standard Truffle icon
    """
    try:
        # Get the standard icon path
        std_icon = get_standard_icon_path()
        
        # Check if both files exist
        if not std_icon.exists():
            return False
            
        if not icon_path.exists():
            return False
            
        # Compare the files
        return filecmp.cmp(icon_path, std_icon, shallow=False)
        
    except Exception as e:
        # Log the error but don't raise it - we want to fall back to dimension validation
        log.detail(f"Error checking whitelist: {str(e)}")
        return False 