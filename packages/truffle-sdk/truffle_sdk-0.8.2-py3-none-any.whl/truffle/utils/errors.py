"""Error handling utilities

This module provides centralized error handling for the Truffle SDK.
"""

import base64
import enum
import json
import os
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, Union, List, Type, Callable

from ..types import UploadError
from ..platform.sdk_pb2 import AppUploadProgress
from .logger import log

class ErrorCode(enum.Enum):
    """Standardized error codes for the Truffle SDK"""
    
    # Authentication errors (100-199)
    AUTHENTICATION_FAILED = 100
    INVALID_CREDENTIALS = 101
    TOKEN_EXPIRED = 102
    PERMISSION_DENIED = 103
    
    # Network errors (200-299)
    CONNECTION_ERROR = 200
    TIMEOUT_ERROR = 201
    SERVER_ERROR = 202
    SERVICE_UNAVAILABLE = 203
    UNAVAILABLE_FOR_LEGAL_REASONS = 204
    
    # File errors (300-399)
    FILE_NOT_FOUND = 300
    FILE_READ_ERROR = 301
    FILE_WRITE_ERROR = 302
    INVALID_FILE_FORMAT = 303
    FILE_TOO_LARGE = 304
    
    # Project errors (400-499)
    INVALID_PROJECT = 400
    MISSING_REQUIRED_FILES = 401
    INVALID_MANIFEST = 402
    BUILD_FAILED = 403
    UPLOAD_FAILED = 404
    
    # Protobuf errors (500-599)
    PROTOBUF_PARSE_ERROR = 500
    PROTOBUF_SERIALIZATION_ERROR = 501
    PROTOBUF_VALIDATION_ERROR = 502
    
    # Validation errors (600-699)
    VALIDATION_ERROR = 600
    INVALID_ARGUMENT = 601
    MISSING_REQUIRED_ARGUMENT = 602
    
    # System errors (700-799)
    SYSTEM_ERROR = 700
    UNEXPECTED_ERROR = 701
    INTERNAL_ERROR = 702
    
    # Unknown error
    UNKNOWN_ERROR = 999
    
    def __str__(self) -> str:
        """Return a human-readable representation of the error code"""
        return f"{self.name} ({self.value})"
    
    @classmethod
    def from_http_status(cls, status_code: int) -> 'ErrorCode':
        """Convert HTTP status code to ErrorCode"""
        if status_code == 401:
            return cls.AUTHENTICATION_FAILED
        elif status_code == 403:
            return cls.PERMISSION_DENIED
        elif status_code == 404:
            return cls.FILE_NOT_FOUND
        elif status_code == 451:
            return cls.UNAVAILABLE_FOR_LEGAL_REASONS
        elif status_code >= 500:
            return cls.SERVER_ERROR
        else:
            return cls.UNKNOWN_ERROR

@dataclass
class ErrorContext:
    """Context information for errors"""
    source: str
    operation: str
    details: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a human-readable representation of the error context"""
        context_str = f"{self.source}.{self.operation}"
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            context_str += f" ({details_str})"
        return context_str

@dataclass
class TruffleError:
    """Base error class for the Truffle SDK"""
    code: ErrorCode
    message: str
    context: Optional[ErrorContext] = None
    details: Optional[Dict[str, Any]] = None
    original_error: Optional[Exception] = None
    
    def __str__(self) -> str:
        """Return a human-readable representation of the error"""
        error_str = f"{self.code}: {self.message}"
        if self.context:
            error_str += f" in {self.context}"
        return error_str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary"""
        result = {
            "code": self.code.value,
            "code_name": self.code.name,
            "message": self.message
        }
        
        if self.context:
            result["context"] = {
                "source": self.context.source,
                "operation": self.context.operation
            }
            if self.context.details:
                result["context"]["details"] = self.context.details
        
        if self.details:
            result["details"] = self.details
            
        if self.original_error:
            result["original_error"] = str(self.original_error)
            
        return result
    
    def to_json(self) -> str:
        """Convert the error to a JSON string"""
        return json.dumps(self.to_dict(), indent=2)

class AuthenticationError(TruffleError):
    """Authentication-related errors"""
    pass

class NetworkError(TruffleError):
    """Network-related errors"""
    pass

class FileError(TruffleError):
    """File-related errors"""
    pass

class ProjectError(TruffleError):
    """Project-related errors"""
    pass

class ProtobufError(TruffleError):
    """Protobuf-related errors"""
    pass

class ValidationError(TruffleError):
    """Validation-related errors"""
    pass

class SystemError(TruffleError):
    """System-related errors"""
    pass

class ErrorHandler:
    """Centralized error handling for the Truffle SDK"""
    
    # Error type mapping
    _error_type_map: Dict[ErrorCode, Type[TruffleError]] = {
        # Authentication errors
        ErrorCode.AUTHENTICATION_FAILED: AuthenticationError,
        ErrorCode.INVALID_CREDENTIALS: AuthenticationError,
        ErrorCode.TOKEN_EXPIRED: AuthenticationError,
        ErrorCode.PERMISSION_DENIED: AuthenticationError,
        
        # Network errors
        ErrorCode.CONNECTION_ERROR: NetworkError,
        ErrorCode.TIMEOUT_ERROR: NetworkError,
        ErrorCode.SERVER_ERROR: NetworkError,
        ErrorCode.SERVICE_UNAVAILABLE: NetworkError,
        ErrorCode.UNAVAILABLE_FOR_LEGAL_REASONS: NetworkError,
        
        # File errors
        ErrorCode.FILE_NOT_FOUND: FileError,
        ErrorCode.FILE_READ_ERROR: FileError,
        ErrorCode.FILE_WRITE_ERROR: FileError,
        ErrorCode.INVALID_FILE_FORMAT: FileError,
        ErrorCode.FILE_TOO_LARGE: FileError,
        
        # Project errors
        ErrorCode.INVALID_PROJECT: ProjectError,
        ErrorCode.MISSING_REQUIRED_FILES: ProjectError,
        ErrorCode.INVALID_MANIFEST: ProjectError,
        ErrorCode.BUILD_FAILED: ProjectError,
        ErrorCode.UPLOAD_FAILED: ProjectError,
        
        # Protobuf errors
        ErrorCode.PROTOBUF_PARSE_ERROR: ProtobufError,
        ErrorCode.PROTOBUF_SERIALIZATION_ERROR: ProtobufError,
        ErrorCode.PROTOBUF_VALIDATION_ERROR: ProtobufError,
        
        # Validation errors
        ErrorCode.VALIDATION_ERROR: ValidationError,
        ErrorCode.INVALID_ARGUMENT: ValidationError,
        ErrorCode.MISSING_REQUIRED_ARGUMENT: ValidationError,
        
        # System errors
        ErrorCode.SYSTEM_ERROR: SystemError,
        ErrorCode.UNEXPECTED_ERROR: SystemError,
        ErrorCode.INTERNAL_ERROR: SystemError,
        
        # Unknown error
        ErrorCode.UNKNOWN_ERROR: TruffleError
    }
    
    @classmethod
    def create_error(cls, 
                    code: ErrorCode, 
                    message: str, 
                    context: Optional[ErrorContext] = None,
                    details: Optional[Dict[str, Any]] = None,
                    original_error: Optional[Exception] = None) -> TruffleError:
        """Create a TruffleError instance
        
        Args:
            code: Error code
            message: Error message
            context: Error context
            details: Additional error details
            original_error: Original exception
            
        Returns:
            TruffleError: The created error
        """
        # Get the appropriate error class
        error_class = cls._error_type_map.get(code, TruffleError)
        
        # Create the error
        return error_class(
            code=code,
            message=message,
            context=context,
            details=details,
            original_error=original_error
        )
    
    @classmethod
    def create_upload_error(cls, code: str, message: str, details: Optional[str] = None) -> UploadError:
        """Create an UploadError instance
        
        Args:
            code: Error code
            message: Error message
            details: Additional error details
            
        Returns:
            UploadError: The created error
        """
        return UploadError(
            code=code,
            message=message,
            details=details
        )
    
    @classmethod
    def create_protobuf_error(cls, raw_error: str) -> AppUploadProgress.AppUploadError:
        """Create a protobuf AppUploadError instance
        
        Args:
            raw_error: Raw error message
            
        Returns:
            AppUploadProgress.AppUploadError: The created error
        """
        return AppUploadProgress.AppUploadError(raw_error=raw_error)
    
    @classmethod
    def decode_error_content(cls, content: str) -> str:
        """Decode error content if it's base64 encoded
        
        Args:
            content: The error content to decode
            
        Returns:
            str: The decoded content
        """
        if not content:
            return content
            
        # Check if content looks like base64
        if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in content):
            try:
                decoded = base64.b64decode(content)
                return decoded.decode('utf-8', errors='replace')
            except Exception as e:
                log.detail(f"Error decoding error content: {str(e)}")
                return content
                
        return content
    
    @classmethod
    def handle_http_error(cls, status_code: int, response_content: str, context: ErrorContext) -> Tuple[bool, Optional[str]]:
        """Handle HTTP errors
        
        Args:
            status_code: HTTP status code
            response_content: Response content
            context: Error context
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Decode the error content if needed
        decoded_content = cls.decode_error_content(response_content)
        
        # Get the error code
        error_code = ErrorCode.from_http_status(status_code)
        
        # Create error message
        if status_code == 451:
            error_message = "Upload unavailable for legal reasons. Please check your authentication and regional restrictions."
        elif status_code == 401:
            error_message = "Authentication failed. Please check your credentials."
        elif status_code == 403:
            error_message = "Permission denied. You don't have permission to perform this operation."
        elif status_code == 404:
            error_message = "Resource not found. The requested resource does not exist."
        elif status_code >= 500:
            error_message = "Server error. The server encountered an error processing your request."
        else:
            error_message = f"HTTP error {status_code}: {decoded_content}"
        
        # Create the error
        error = cls.create_error(
            code=error_code,
            message=error_message,
            context=context,
            details={"status_code": status_code, "response_content": decoded_content}
        )
        
        # Log the error
        log.error(f"HTTP error {status_code} in {context}")
        log.detail(f"Error content: {decoded_content}")
        
        return False, str(error)
    
    @classmethod
    def handle_exception(cls, e: Exception, context: ErrorContext) -> Tuple[bool, Optional[str]]:
        """Handle exceptions
        
        Args:
            e: The exception
            context: Error context
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Get stack trace
        stack_trace = traceback.format_exc()
        context.stack_trace = stack_trace
        
        # Determine error code and message
        if isinstance(e, ValueError):
            error_code = ErrorCode.VALIDATION_ERROR
            error_message = str(e)
        elif isinstance(e, ConnectionError):
            error_code = ErrorCode.CONNECTION_ERROR
            error_message = f"Connection error: {str(e)}. Please check your internet connection."
        elif isinstance(e, TimeoutError):
            error_code = ErrorCode.TIMEOUT_ERROR
            error_message = f"Operation timed out: {str(e)}"
        elif isinstance(e, FileNotFoundError):
            error_code = ErrorCode.FILE_NOT_FOUND
            error_message = f"File not found: {str(e)}"
        elif isinstance(e, PermissionError):
            error_code = ErrorCode.PERMISSION_DENIED
            error_message = f"Permission denied: {str(e)}"
        elif isinstance(e, json.JSONDecodeError):
            error_code = ErrorCode.INVALID_FILE_FORMAT
            error_message = f"Invalid JSON format: {str(e)}"
        else:
            error_code = ErrorCode.UNEXPECTED_ERROR
            error_message = f"Unexpected error: {str(e)}"
        
        # Create the error
        error = cls.create_error(
            code=error_code,
            message=error_message,
            context=context,
            details={"exception_type": type(e).__name__},
            original_error=e
        )
        
        # Log the error
        log.error(f"Exception in {context}: {str(e)}")
        log.detail(stack_trace)
        
        return False, str(error)
    
    @classmethod
    def handle_project_error(cls, path: Path, missing_files: List[str]) -> Tuple[bool, Optional[str]]:
        """Handle project validation errors
        
        Args:
            path: Path to the project directory
            missing_files: List of missing required files
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="ProjectValidator",
            operation="validate_project",
            details={"path": str(path), "missing_files": missing_files}
        )
        
        # Create error message
        error_message = f"Not a valid Truffle project directory (missing: {', '.join(missing_files)})"
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.MISSING_REQUIRED_FILES,
            message=error_message,
            context=context
        )
        
        # Log the error
        log.error(f"Invalid project directory: {path}")
        log.detail(f"Missing files: {', '.join(missing_files)}")
        
        return False, str(error)
    
    @classmethod
    def handle_manifest_error(cls, path: Path, error_message: str) -> Tuple[bool, Optional[str]]:
        """Handle manifest validation errors
        
        Args:
            path: Path to the manifest file
            error_message: Error message
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="ProjectValidator",
            operation="validate_manifest",
            details={"path": str(path)}
        )
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.INVALID_MANIFEST,
            message=error_message,
            context=context
        )
        
        # Log the error
        log.error(f"Invalid manifest: {path}")
        log.detail(error_message)
        
        return False, str(error)
    
    @classmethod
    def handle_protobuf_error(cls, data: bytes, error_message: str) -> Tuple[bool, Optional[str]]:
        """Handle protobuf parsing errors
        
        Args:
            data: Raw data that failed to parse
            error_message: Error message
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="ProgressTracker",
            operation="parse_protobuf",
            details={"data_length": len(data) if data else 0}
        )
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.PROTOBUF_PARSE_ERROR,
            message=error_message,
            context=context
        )
        
        # Log the error
        log.error("Failed to parse protobuf message")
        log.detail(error_message)
        
        return False, str(error)
    
    @classmethod
    def handle_upload_error(cls, file_path: Path, error_message: str) -> Tuple[bool, Optional[str]]:
        """Handle upload errors
        
        Args:
            file_path: Path to the file that failed to upload
            error_message: Error message
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="Uploader",
            operation="upload_file",
            details={"file_path": str(file_path)}
        )
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.UPLOAD_FAILED,
            message=error_message,
            context=context
        )
        
        # Log the error
        log.error(f"Upload failed: {file_path}")
        log.detail(error_message)
        
        return False, str(error)
    
    @classmethod
    def handle_build_error(cls, path: Path, error_message: str) -> Tuple[bool, Optional[str]]:
        """Handle build errors
        
        Args:
            path: Path to the project directory
            error_message: Error message
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="BuildCommand",
            operation="build_project",
            details={"path": str(path)}
        )
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.BUILD_FAILED,
            message=error_message,
            context=context
        )
        
        # Log the error
        log.error(f"Build failed: {path}")
        log.detail(error_message)
        
        return False, str(error)
    
    @classmethod
    def handle_user_id_error(cls) -> Tuple[bool, Optional[str]]:
        """Handle user ID errors
        
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Create error context
        context = ErrorContext(
            source="Uploader",
            operation="_get_user_id"
        )
        
        # Create the error
        error = cls.create_error(
            code=ErrorCode.AUTHENTICATION_FAILED,
            message="No user ID found. Please make sure you are logged in.",
            context=context
        )
        
        # Log the error
        log.error("Authentication failed")
        log.detail("No user ID found. Please make sure you are logged in.")
        
        return False, str(error) 