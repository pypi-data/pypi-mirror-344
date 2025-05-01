"""
CLI Logging System

This module implements a rich console logging system for the Truffle CLI:
- Provides color-coded output with consistent styling
- Implements structured logging with indentation and grouping
- Supports progress tracking and metrics display
- Handles formatting with details and context
- Manages terminal output with minimal flicker
"""

import warnings
import requests.packages.urllib3
import logging

# --- Filter specific warnings --- 
# Ignore duplicate name warnings from zipfile (often related to manifest)
# TODO: Fix the root cause in create_zip_bundle where manifest.json might be added twice.
warnings.filterwarnings('ignore', category=UserWarning, module='zipfile')
# Ignore warnings about unverified HTTPS requests (common when verify=False is used)
# TODO: Implement proper certificate verification or explicit trust for HTTPS requests instead of using verify=False.
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Filter out pip's installation messages
logging.getLogger('pip').setLevel(logging.WARNING)
logging.getLogger('pip._internal').setLevel(logging.WARNING)
logging.getLogger('pip._vendor').setLevel(logging.WARNING)

# --- End warning filters ---

from dataclasses import dataclass
from typing import Optional, Dict, List, Union, Deque
from collections import deque
import sys
import os
import time

__all__ = ['Colors', 'Symbols', 'Logger', 'log']

# Replace TypedDict with a regular Dict for Python 3.10 compatibility
DetailDict = Dict[str, Union[str, int, float]]

@dataclass
class Colors:
    """ANSI color codes for terminal output with Truffle-specific styling."""
    __slots__ = []
   
    MAIN: str = "\033[38;2;95;173;235m"      # #5FADEB - Primary actions/success
    SECONDARY: str = "\033[38;2;74;155;217m"  # #4A9BD9 - Info/progress
    WHITE: str = "\033[38;2;255;255;255m"     # #FFFFFF - Standard output
    LIGHT_GRAY: str = "\033[38;2;204;204;204m"# #CCCCCC - Secondary info
    DIM_GRAY: str = "\033[38;2;128;128;128m"  # #808080 - Technical details
    SILVER: str = "\033[38;2;220;220;220m"    # #DCDCDC - Very subtle effects
    WHISPER: str = "\033[38;2;240;240;240m"   # #F0F0F0 - Nearly white, super subtle
    ERROR: str = "\033[38;2;255;59;48m"       # #FF3B30 - Errors
    WARNING: str = "\033[38;2;255;149;0m"     # #FF9500 - Warnings
    RESET: str = "\033[0m"

    # Background colors for blocks
    ERROR_BG: str = "\033[48;2;255;59;48;0.1m"
    WARNING_BG: str = "\033[48;2;255;149;0;0.1m"
    
    # Terminal control
    CLEAR_SCREEN: str = "\033[H\033[2J"
    CLEAR_LINE: str = "\033[K"
    MOVE_TO_TOP: str = "\033[H"

@dataclass
class Symbols:
    """Unicode symbols for consistent logging with Truffle-specific styling."""
    __slots__ = []
   
    # Status indicators
    SUCCESS: str = "✓"
    ERROR: str = "✗"
    WARNING: str = "!"
    CHECK: str = "✓"
    ARROW: str = "→"
    INFO: str = "ℹ"
    LOADING: str = "⟳"
   
    # File operations
    FILE_CREATED: str = "+"
    FILE_MODIFIED: str = "•"
    FILE_DELETED: str = "-"
    FILE_COPIED: str = "↗"
   
    # Command
    CMD_PREFIX: str = "$"
    
    # Progress
    PROGRESS_FILLED: str = "█"
    PROGRESS_EMPTY: str = "░"
    
    # Navigation
    UP: str = "↑"
    DOWN: str = "↓"
    LEFT: str = "←"
    RIGHT: str = "→"

class Logger:
    """
    Beautiful CLI logger with Truffle-specific styling.
   
    Features:
    - Color-coded output with consistent styling
    - Indentation and grouping for structured logs
    - Version and metric formatting
    - Progress tracking and display
    - Chainable methods for fluent API
    - Terminal-aware output with minimal flicker
    """
   
    def __init__(self) -> None:
        self._indent_level: int = 0
        self._indent_size: int = 2
        self._indent_cache: Dict[int, str] = {}
        self._last_update_time: float = 0
        self._update_interval: float = 0.05  # 50ms between updates
        self._terminal_width: int = self._get_terminal_width()
        self._terminal_height: int = self._get_terminal_height()
        self._log_buffer: Deque[str] = deque(maxlen=10)
        self._progress_bar: Optional[ProgressBar] = None
        self._details: Dict[str, DetailDict] = {}
    
    def _get_terminal_width(self) -> int:
        """Get the terminal width with fallback."""
        try:
            return os.get_terminal_size().columns
        except:
            return 80  # Default fallback
    
    def _get_terminal_height(self) -> int:
        """Get the terminal height with fallback."""
        try:
            return os.get_terminal_size().lines
        except:
            return 24  # Default fallback
   
    def _indent(self) -> str:
        """Generate indentation string based on current level."""
        if self._indent_level not in self._indent_cache:
            self._indent_cache[self._indent_level] = " " * (self._indent_level * self._indent_size)
        return self._indent_cache[self._indent_level]
   
    def _format_version(self, version: str) -> str:
        """Format version string to vX.Y.Z format."""
        return f"v{version}" if not version.startswith('v') else version
   
    def _format(self,
                color: str,
                message: str,
                prefix: str = "",
                suffix: str = "",
                version: Optional[str] = None,
                metric: Optional[str] = None,
                end: str = "\n") -> 'Logger':
        """Format and print a log message with consistent styling."""
        indent = self._indent()
        prefix = f"{prefix} " if prefix else ""
        parts: List[str] = [f"{color}{indent}{prefix}{message}{Colors.RESET}"]
       
        if suffix:
            parts.append(suffix)
        if version:
            parts.append(f"{Colors.DIM_GRAY} {self._format_version(version)}{Colors.RESET}")
        if metric:
            parts.append(f"{Colors.DIM_GRAY}{metric}{Colors.RESET}")
           
        print(" ".join(parts), end=end, file=sys.stderr)
        return self
    
    def _should_update(self) -> bool:
        """Check if enough time has passed to update the display."""
        current_time = time.time()
        if current_time - self._last_update_time >= self._update_interval:
            self._last_update_time = current_time
            return True
        return False
   
    def cmd(self, command: str, args: Optional[str] = None) -> 'Logger':
        """Format command input styling."""
        parts: List[str] = [f"{Colors.MAIN}{Symbols.CMD_PREFIX} {command}{Colors.RESET}"]
        if args:
            parts.append(f"{Colors.WHITE}{args}{Colors.RESET}")
        print(" ".join(parts), file=sys.stderr)
        return self
   
    def main(self, message: str, version: Optional[str] = None) -> 'Logger':
        """Log main/primary actions in blue."""
        return self._format(Colors.MAIN, message, version=version)
   
    def build(self, message: str, version: Optional[str] = None) -> 'Logger':
        """Log build messages in secondary blue."""
        return self._format(Colors.SECONDARY, message, version=version)
   
    def detail(self, message: str, metric: Optional[str] = None, dim_suffix: Optional[str] = None) -> 'Logger':
        """Log additional details in light gray."""
        msg = message
        if dim_suffix:
            msg = f"{message} ({dim_suffix})"
        return self._format(Colors.LIGHT_GRAY, msg, metric=metric)
   
    def success(self, message: str) -> 'Logger':
        """Log success messages in main blue with checkmark."""
        return self._format(Colors.MAIN, f"{Symbols.SUCCESS} {message}")
   
    def prompt(self, label: str, value: str = "", end: str = "\n") -> 'Logger':
        """Format input prompt styling."""
        return self._format(
            Colors.MAIN,
            f"{Symbols.ARROW} {label}: ",
            suffix=f" {Colors.WHITE}{value}{Colors.RESET}" if value else "",
            end=end
        )
   
    def created_file(self, path: str) -> 'Logger':
        """Log file creation indicator."""
        return self._format(Colors.MAIN, f"{Symbols.FILE_CREATED} {path}")
   
    def modified_file(self, path: str) -> 'Logger':
        """Log file modification indicator."""
        return self._format(Colors.MAIN, f"{Symbols.FILE_MODIFIED} {path}")
   
    def deleted_file(self, path: str) -> 'Logger':
        """Log file deletion indicator."""
        return self._format(Colors.MAIN, f"{Symbols.FILE_DELETED} {path}")
    
    def copied_file(self, src: str, dst: str) -> 'Logger':
        """Log file copy operation."""
        return self._format(Colors.MAIN, f"{Symbols.FILE_COPIED} {src} → {dst}")
   
    def check(self, item: str, version: Optional[str] = None) -> 'Logger':
        """Log validation checkmark with optional version."""
        return self._format(Colors.MAIN, f"{Symbols.CHECK} {item}", version=version)
   
    def metric(self, value: Union[str, int, float], context: Optional[str] = None) -> 'Logger':
        """Log metric display with optional context in light gray."""
        msg = str(value)
        if context:
            msg = f"{msg} {context}"
        return self.detail(msg)  # Just use detail's light gray color

    def error(self, message: str) -> 'Logger':
        """Log error messages in red with error symbol."""
        return self._format(Colors.ERROR, f"{Symbols.ERROR} {message}")

    def warning(self, message: str) -> 'Logger':
        """Log warning messages in orange with warning symbol."""
        return self._format(Colors.WARNING, f"{Symbols.WARNING} {message}")
    
    def info(self, message: str) -> 'Logger':
        """Log info messages in secondary blue with info symbol."""
        return self._format(Colors.SECONDARY, f"{Symbols.INFO} {message}")
    
    def loading(self, message: str) -> 'Logger':
        """Log loading messages with spinner symbol."""
        return self._format(Colors.SECONDARY, f"{Symbols.LOADING} {message}")

    def debug(self, message: str) -> 'Logger':
        """Log debug messages in dim gray."""
        return self._format(Colors.DIM_GRAY, f"{Symbols.INFO} {message}")

    def trace(self, message: str) -> 'Logger':
        """Log trace messages in very dim gray - lowest level of logging."""
        # Only log if TRUFFLE_TRACE environment variable is set
        if os.environ.get('TRUFFLE_TRACE'):
            return self._format(Colors.DIM_GRAY, f"• {message}")
        return self

    def group(self, message: str) -> 'Logger':
        """Create a new log group with increased indentation."""
        self._format(Colors.MAIN, message)
        self._indent_level += 1
        return self

    def end_group(self) -> 'Logger':
        """End the current log group and decrease indentation."""
        if self._indent_level > 0:
            self._indent_level -= 1
        return self

    def __enter__(self) -> 'Logger':
        """Context manager entry - no-op since indentation is handled by group()."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - decrease indentation level."""
        self.end_group()
    
    def add_to_buffer(self, message: str) -> 'Logger':
        """Add a message to the log buffer for display."""
        self._log_buffer.append(message)
        if self._should_update():
            self._redraw_buffer()
        return self
    
    def _redraw_buffer(self) -> None:
        """Redraw the log buffer with minimal flicker."""
        # Clear screen and move to top
        sys.stderr.write(Colors.CLEAR_SCREEN)
        
        # Print logs with proper spacing
        for log in self._log_buffer:
            sys.stderr.write(f"{log}\n")
        
        # Add padding for progress bar
        sys.stderr.write("\n")
        sys.stderr.flush()
    
    def clear_buffer(self) -> 'Logger':
        """Clear the log buffer."""
        self._log_buffer.clear()
        return self
    
    def set_progress_bar(self, progress_bar: 'ProgressBar') -> 'Logger':
        """Set the progress bar for this logger."""
        self._progress_bar = progress_bar
        return self
    
    def update_progress(self, progress: float) -> 'Logger':
        """Update the progress bar if one is set."""
        if self._progress_bar and self._should_update():
            self._progress_bar.update(progress)
        return self

class ProgressBar:
    """
    Progress bar implementation with smooth animation.
    
    Features:
    - Fixed width with customizable characters
    - Smooth animation with buffering
    - Minimal terminal updates
    - Consistent styling with the logger
    """
    
    def __init__(self, width: int = 50):
        self.width = width
        self.last_progress: float = 0.0
        self.last_update: float = 0
        self.update_interval: float = 0.05  # 50ms between updates
        self.buffer_size: float = 0.1  # 10% buffer for smooth animation
    
    def _get_progress_chars(self, progress: float) -> str:
        """Get the progress bar characters."""
        filled = int(self.width * progress)
        return Symbols.PROGRESS_FILLED * filled + Symbols.PROGRESS_EMPTY * (self.width - filled)
    
    def update(self, progress: float) -> None:
        """Update the progress bar with buffering."""
        current_time = time.time()
        if current_time - self.last_update < self.update_interval:
            return
            
        # Apply buffering for smooth animation
        target_progress = min(progress + self.buffer_size, 1.0)
        current_progress = self.last_progress + (target_progress - self.last_progress) * 0.3
        
        # Only update if there's meaningful change
        if abs(current_progress - self.last_progress) < 0.001:
            return
            
        self.last_progress = current_progress
        self.last_update = current_time
        
        # Calculate percentage
        percentage = int(current_progress * 100)
        
        # Get progress bar
        progress_chars = self._get_progress_chars(current_progress)
        
        # Clear the progress bar line
        sys.stderr.write(Colors.CLEAR_LINE)
        
        # Format the output with main blue color and proper padding
        output = f"{Colors.MAIN}[{progress_chars}] {percentage}%{Colors.RESET}"
        sys.stderr.write(output)
        sys.stderr.flush()

# Global logger instance
log = Logger() 

class UploadLogger:
    """Upload-specific logger that respects LOG_LEVEL environment variable.
    
    Log Levels:
    1 = INFO (default) - Basic progress and status
    2 = DETAIL - More detailed operation info
    3 = DEBUG - Developer debugging info
    4 = TRACE - Everything, including pip and system messages
    """
    
    def should_log(self, level: int) -> bool:
        """Check if we should log at this level.
        
        Args:
            level: The level to check (1=info, 2=detail, 3=debug, 4=trace)
            
        Returns:
            bool: True if we should log at this level
        """
        current_level = int(os.environ.get('LOG_LEVEL', '1'))
        return level <= current_level
    
    def info(self, message: str, level: int = 1) -> None:
        """Log info message if level matches."""
        if self.should_log(level):
            log.info(message)
    
    def detail(self, message: str, level: int = 2) -> None:
        """Log detail message if level matches."""
        if self.should_log(level):
            log.detail(message)
    
    def debug(self, message: str, level: int = 3) -> None:
        """Log debug message if level matches."""
        if self.should_log(level):
            log.debug(message)
            
    def trace(self, message: str) -> None:
        """Log trace message (level 4) - includes all system and pip messages."""
        if self.should_log(4):
            log.detail(f"TRACE: {message}")
    
    def success(self, message: str) -> None:
        """Always log success messages."""
        log.success(message)
    
    def error(self, message: str) -> None:
        """Always log error messages."""
        log.error(message)
    
    def warning(self, message: str) -> None:
        """Always log warning messages."""
        log.warning(message)

# Create a global instance
upload_log = UploadLogger() 