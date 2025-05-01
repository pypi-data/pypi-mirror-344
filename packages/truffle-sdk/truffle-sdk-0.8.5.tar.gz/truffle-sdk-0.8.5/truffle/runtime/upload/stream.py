"""Real-time stream management for upload progress

This module implements a high-performance stream manager for handling SSE updates
with minimal overhead and efficient progress tracking.
"""

import sys
import time
from typing import Optional, Deque
from collections import deque
from dataclasses import dataclass
from ...utils.logger import log, Colors, Symbols
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

class StreamManager:
    """High-performance SSE stream manager for AppUploadProgress
    
    Features:
    - Fixed-size circular buffer for logs
    - Pre-computed strings for UI elements
    - Minimal string operations
    - Single write operations
    - Memory-efficient log storage
    - Timeout detection
    - Full support for AppUploadProgress steps
    """
    
    def __init__(self, max_logs: int = 6, timeout: int = 300):
        self.progress_bar = ProgressBar()
        self.last_step = AppUploadProgress.UploadStep.STEP_UNKNOWN
        self._logs: Deque[str] = deque(maxlen=max_logs)
        self._main = Colors.MAIN
        self._detail = Colors.LIGHT_GRAY
        self._error = Colors.ERROR
        self._warning = Colors.WARNING
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
    
    def update_progress(self, progress: AppUploadProgress) -> None:
        """Update progress with minimal operations"""
        # Update last activity time
        self.last_update_time = time.time()
        
        # Step change - efficient string comparison
        if progress.step != self.last_step:
            step_desc = self._step_descriptions.get(progress.step, "Processing...")
            self._add_log(step_desc, self._main)
            self.last_step = progress.step
            
        # Error handling
        if progress.error and progress.error.raw_error:
            self._add_log(progress.error.raw_error, self._error)
            return
            
        # Progress update - convert from 0-100 to 0-1 range
        self.progress_bar.update(progress.progress / 100.0)
        
        # Log message and substep
        if progress.latest_logs:
            self._add_log(progress.latest_logs, self._detail)
        if progress.substep:
            self._add_log(f"  → {progress.substep}", self._detail)
    
    def check_timeout(self) -> bool:
        """Check if the upload has timed out or stalled"""
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        
        # Check for timeout
        if elapsed > self.timeout:
            self._add_log("Upload timed out", self._error)
            return True
            
        # Check for stalled upload (no updates for a while)
        if elapsed > self.stalled_threshold:
            self._add_log(f"Upload appears stalled (no updates for {int(elapsed)} seconds)", self._warning)
            return False
            
        return False
            
    def _add_log(self, message: str, color: str) -> None:
        """Add log entry with color"""
        self._logs.append(f"{color}{message}{Colors.RESET}")
        self._redraw_logs()
        
    def _redraw_logs(self) -> None:
        """Redraw logs with minimal operations"""
        # Clear screen and move to top
        sys.stderr.write("\033[H\033[2J")
        
        # Single write operation for all logs
        sys.stderr.write("\n".join(self._logs) + "\n\n")
        sys.stderr.flush() 