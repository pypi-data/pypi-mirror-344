"""Upload progress tracking with optimized protobuf parsing

This module implements efficient progress tracking with optimized operations
for protobuf parsing and state management.
"""

import base64
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from google.protobuf import message
from ...utils.logger import log
from ...types import UploadProgress, UploadError, UploadState
# Import the actual protobuf classes
from ...platform.sdk_pb2 import AppUploadProgress

@dataclass
class UploadTracker:
    """High-performance upload progress tracker
    
    Features:
    - Efficient protobuf parsing
    - Optimized state management
    - Minimal memory allocations
    - Pre-computed step mappings
    """
    
    current_step: int = AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE
    progress: float = 0.0
    
    def parse_progress(self, data: bytes) -> UploadProgress:
        """Parse protobuf message with minimal allocations"""
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
            # Update internal state
            self.current_step = step
            self.progress = progress_msg.progress / 100.0

            # Directly use the type from the proto message
            upload_type = progress_msg.type if progress_msg.HasField('type') else None
            
            # Create progress update with direct proto enum values (ints)
            return UploadProgress(
                step=step,
                progress=self.progress,
                message=progress_msg.latest_logs,
                error=progress_msg.error.raw_error if progress_msg.HasField('error') else None,
                substep=progress_msg.substep if progress_msg.HasField('substep') else None,
                type=upload_type
            )
            
        except Exception as e:
            log.error("Failed to parse progress update")
            log.detail(str(e))
            # Use current internal state for error reporting
            return UploadProgress(
                step=self.current_step,
                progress=self.progress,
                message="Error parsing progress update",
                error=str(e)
            )
    
    def _parse_protobuf(self, data: bytes) -> AppUploadProgress:
        """Parse protobuf message with error handling"""
        try:
            # Use the actual protobuf message class
            progress_msg = AppUploadProgress()
            progress_msg.ParseFromString(data)
            return progress_msg
        except Exception as e:
            raise ValueError(f"Failed to parse protobuf: {e}")
            
    def get_state(self) -> UploadState:
        """Get current upload state with minimal allocations"""
        # Use current internal state (which now uses proto enum ints)
        return UploadState(
            step=self.current_step,
            progress=self.progress,
            message="",
            error=None,
            logs=[]
        ) 