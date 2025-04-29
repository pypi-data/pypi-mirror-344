"""Unified progress tracking for uploads

This module provides a comprehensive progress tracking system for uploads,
combining efficient protobuf parsing, state management, and UI rendering.
"""

import sys
import time
import base64
from typing import Optional, Dict, Deque, Callable, Any
from collections import deque
from dataclasses import dataclass, field
from google.protobuf import message

from ...utils.logger import log, Colors, Symbols
from ...types import UploadProgress, UploadError, UploadState
from ...platform.sdk_pb2 import AppUploadProgress

@dataclass
class ProgressBar:
    """Optimized progress bar implementation with efficient updates"""
    width: int = 50
    last_progress: float = 0.0
    _buffer: str = ""
    start_time: float = 0.0
    
    def __post_init__(self):
        """Initialize static elements for efficient rendering"""
        self._empty_bar = "░" * self.width
        self._reset = Colors.RESET
        self._main = Colors.MAIN
        self.start_time = time.time()
    
    def update(self, progress: float) -> None:
        """Update progress bar with minimal string operations"""
        if abs(progress - self.last_progress) < 0.001:
            return
            
        # Calculate filled width once
        filled = int(self.width * progress)
        
        # Use pre-computed strings for efficient rendering
        bar = "█" * filled + self._empty_bar[filled:]
        percentage = int(progress * 100)
        
        # Calculate elapsed time
        elapsed = time.time() - self.start_time
        elapsed_str = self._format_time(elapsed)
        
        # Single write operation for terminal output
        sys.stderr.write(f"\033[K{self._main}[{bar}] {percentage}% {elapsed_str}{self._reset}")
        sys.stderr.flush()
        
        self.last_progress = progress
    
    def _format_time(self, seconds: float) -> str:
        """Format elapsed time in a human-readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        minutes = int(seconds / 60)
        seconds = seconds % 60
        return f"{minutes}m {seconds:.0f}s"

class ProgressTracker:
    """Unified progress tracking system for uploads
    
    Features:
    - Efficient protobuf parsing
    - Optimized state management
    - Minimal memory allocations
    - Pre-computed step mappings
    - Fixed-size circular buffer for logs
    - Pre-computed strings for UI elements
    - Minimal string operations
    - Single write operations
    - Memory-efficient log storage
    - Timeout detection
    - Full support for AppUploadProgress steps
    """
    
    def __init__(self, max_logs: int = 6, timeout: int = 300, show_progress_bar: bool = True):
        """Initialize the progress tracker
        
        Args:
            max_logs: Maximum number of logs to keep
            timeout: Timeout in seconds
            show_progress_bar: Whether to show the progress bar
        """
        # State tracking
        self.current_step: int = AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE
        self.progress: float = 0.0
        
        # UI elements
        self.show_progress_bar = show_progress_bar
        self.progress_bar = ProgressBar() if show_progress_bar else None
        self._logs: Deque[str] = deque(maxlen=max_logs)
        self._main = Colors.MAIN
        self._detail = Colors.LIGHT_GRAY
        self._error = Colors.ERROR
        self._warning = Colors.WARNING
        
        # Timeout tracking
        self.timeout = timeout
        self.last_update_time = time.time()
        self.stalled_threshold = 30  # Seconds without updates to consider stalled
        
        # Pre-compute step descriptions for efficiency
        self._step_descriptions = {
            AppUploadProgress.UploadStep.STEP_UNKNOWN: "Initializing...",
            AppUploadProgress.UploadStep.STEP_UPLOAD_BUNDLE: "Uploading bundle...",
            AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE: "Verifying bundle...",
            AppUploadProgress.UploadStep.STEP_SYNC_WITH_SERVER: "Syncing with server...",
            AppUploadProgress.UploadStep.STEP_WRITE_BUNDLE: "Writing bundle...",
            AppUploadProgress.UploadStep.STEP_CREATE_CONTAINER: "Creating container...",
            AppUploadProgress.UploadStep.STEP_INSTALL_DEPENDENCIES: "Installing dependencies...",
            AppUploadProgress.UploadStep.STEP_GENERATE_CLASSIFIER_DATA: "Generating classifier data...",
            AppUploadProgress.UploadStep.STEP_SAVE_CONTAINER: "Saving container...",
            AppUploadProgress.UploadStep.STEP_GATHER_TOOLS: "Gathering tools...",
            AppUploadProgress.UploadStep.STEP_VERIFY_INSTALL: "Verifying installation...",
            AppUploadProgress.UploadStep.STEP_INTALLED: "Installation complete!"
        }
    
    def parse_progress(self, data: bytes) -> UploadProgress:
        """Parse protobuf message with minimal allocations
        
        Args:
            data: Raw data to parse
            
        Returns:
            UploadProgress: Parsed progress update
        """
        try:
            # Remove null bytes efficiently
            while data.endswith(b'\0'):
                data = data[:-1]
                
            # Try to base64 decode the data if it looks like base64
            try:
                if data and all(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data):
                    data = base64.b64decode(data)
                    # Remove null bytes after decoding
                    while data.endswith(b'\0'):
                        data = data[:-1]
            except Exception as e:
                log.detail(f"Error decoding base64 data: {str(e)}")
                # Continue with original data if decoding fails
                
            # Parse protobuf message
            progress_msg = self._parse_protobuf(data)
            
            # Directly use the step from the proto message
            step = progress_msg.step
            
            # Create progress update with direct proto enum value (int)
            return UploadProgress(
                step=step,
                progress=progress_msg.progress / 100.0,
                message=progress_msg.latest_logs,
                error=progress_msg.error.raw_error if progress_msg.HasField('error') else None
            )
            
        except Exception as e:
            log.error("Failed to parse progress update")
            log.detail(str(e))
            return UploadProgress(
                step=self.current_step,
                progress=self.progress,
                message="Error parsing progress update",
                error=str(e)
            )
    
    def _parse_protobuf(self, data: bytes) -> AppUploadProgress:
        """Parse protobuf message with error handling
        
        Args:
            data: Raw data to parse
            
        Returns:
            AppUploadProgress: Parsed protobuf message
            
        Raises:
            ValueError: If parsing fails
        """
        try:
            # Use the actual protobuf message class
            progress_msg = AppUploadProgress()
            progress_msg.ParseFromString(data)
            return progress_msg
        except Exception as e:
            raise ValueError(f"Failed to parse protobuf: {e}")
    
    def update_progress(self, progress: AppUploadProgress) -> None:
        """Update progress tracking with UI updates
        
        Args:
            progress: Progress update from the server
        """
        # Update last update time
        self.last_update_time = time.time()
        
        # Update step directly
        self.current_step = progress.step
        
        # Update progress
        self.progress = progress.progress / 100.0
        
        # Update UI if progress bar is enabled
        if self.show_progress_bar and self.progress_bar:
            self.progress_bar.update(self.progress)
        
        # Add log message
        if progress.latest_logs:
            self._add_log(progress.latest_logs, self._detail)
        
        # Check for errors
        if progress.HasField('error'):
            error_msg = progress.error.raw_error
            self._add_log(f"Error: {error_msg}", self._error)
            
        # Check for completion
        if progress.step == AppUploadProgress.UploadStep.STEP_INTALLED:
            self._add_log("Upload completed successfully!", self._main)
    
    def check_timeout(self) -> bool:
        """Check if the upload has timed out
        
        Returns:
            bool: True if the upload has timed out
        """
        elapsed = time.time() - self.last_update_time
        
        # Check for timeout
        if elapsed > self.timeout:
            self._add_log(f"Upload timed out after {self.timeout} seconds", self._error)
            return True
            
        # Check for stalled upload
        if elapsed > self.stalled_threshold:
            self._add_log(f"Upload stalled for {int(elapsed)} seconds", self._warning)
            
        return False
    
    def _add_log(self, message: str, color: str) -> None:
        """Add a log message
        
        Args:
            message: Log message
            color: Color to use for the message
        """
        self._logs.append(f"{color}{message}{Colors.RESET}")
        self._redraw_logs()
    
    def _redraw_logs(self) -> None:
        """Redraw the log display"""
        # Clear the screen
        sys.stderr.write("\033[2J\033[H")
        
        # Redraw progress bar if enabled
        if self.show_progress_bar and self.progress_bar:
            self.progress_bar.update(self.progress)
        
        # Redraw logs
        for log in self._logs:
            sys.stderr.write(f"{log}\n")
        
        sys.stderr.flush()
    
    def get_state(self) -> UploadState:
        """Get current upload state with minimal allocations
        
        Returns:
            UploadState: Current upload state
        """
        return UploadState(
            step=self.current_step,
            progress=self.progress,
            message=self._step_descriptions.get(self.current_step, "Unknown state"),
            error=None,
            logs=list(self._logs)
        ) 