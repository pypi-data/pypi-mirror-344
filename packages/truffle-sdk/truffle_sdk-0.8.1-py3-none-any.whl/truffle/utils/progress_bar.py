"""
Progress bar utility for Truffle SDK.

This module provides a smooth, fluid progress bar implementation that can be used
across the Truffle SDK. It handles interpolation between updates to ensure a
smooth animation even when updates are infrequent.
"""

import time
import math
from typing import Optional, Callable, Dict, Any, List, Tuple
from dataclasses import dataclass
from threading import Lock

@dataclass
class ProgressBarConfig:
    """Configuration for the progress bar."""
    width: int = 40
    fill_char: str = "█"
    empty_char: str = "░"
    show_percentage: bool = True
    show_elapsed_time: bool = True
    animation_speed: float = 0.1  # seconds between animation frames
    interpolation_factor: float = 0.2  # how quickly to interpolate to target (0-1)
    min_update_interval: float = 0.05  # minimum time between updates in seconds

class SmoothProgressBar:
    """
    A smooth, fluid progress bar implementation.
    
    This progress bar interpolates between progress updates to ensure a smooth
    animation even when updates are infrequent. It also handles rate limiting
    to prevent too frequent updates.
    """
    
    def __init__(
        self,
        config: Optional[ProgressBarConfig] = None,
        on_update: Optional[Callable[[float], None]] = None
    ):
        """
        Initialize the progress bar.
        
        Args:
            config: Configuration for the progress bar
            on_update: Callback function to call when the progress bar updates
        """
        self.config = config or ProgressBarConfig()
        self.on_update = on_update
        
        # Current state
        self._target_progress = 0.0  # The actual progress value from the server
        self._display_progress = 0.0  # The interpolated progress value for display
        self._start_time = time.time()
        self._last_update_time = time.time()
        self._last_render_time = time.time()
        self._lock = Lock()
        
        # Animation state
        self._animation_running = False
        self._animation_thread = None
    
    def update(self, progress: float) -> None:
        """
        Update the progress bar with a new progress value.
        
        Args:
            progress: Progress value between 0 and 1
        """
        with self._lock:
            # Clamp progress to [0, 1]
            self._target_progress = max(0.0, min(1.0, progress))
            self._last_update_time = time.time()
            
            # Start animation if not already running
            if not self._animation_running:
                self._start_animation()
    
    def _start_animation(self) -> None:
        """Start the animation loop."""
        self._animation_running = True
        self._animate()
    
    def _animate(self) -> None:
        """Animation loop that interpolates between progress values."""
        while self._animation_running:
            with self._lock:
                # Check if we need to update
                current_time = time.time()
                if current_time - self._last_render_time < self.config.min_update_interval:
                    continue
                
                # Interpolate towards target progress
                if abs(self._display_progress - self._target_progress) > 0.001:
                    # Use smooth easing function for more natural animation
                    diff = self._target_progress - self._display_progress
                    self._display_progress += diff * self.config.interpolation_factor
                    
                    # Render the progress bar
                    self._render()
                    self._last_render_time = current_time
                elif self._display_progress >= 1.0:
                    # Animation complete
                    self._animation_running = False
                    break
            
            # Sleep to control animation speed
            time.sleep(self.config.animation_speed)
    
    def _render(self) -> None:
        """Render the progress bar."""
        # Calculate filled width
        filled_width = int(self._display_progress * self.config.width)
        empty_width = self.config.width - filled_width
        
        # Build the progress bar string
        progress_bar = self.config.fill_char * filled_width + self.config.empty_char * empty_width
        
        # Add percentage if enabled
        if self.config.show_percentage:
            percentage = int(self._display_progress * 100)
            progress_bar = f"{progress_bar} {percentage}%"
        
        # Add elapsed time if enabled
        if self.config.show_elapsed_time:
            elapsed = int(time.time() - self._start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            progress_bar = f"{progress_bar} [{time_str}]"
        
        # Call the update callback if provided
        if self.on_update:
            self.on_update(self._display_progress)
    
    def reset(self) -> None:
        """Reset the progress bar to 0."""
        with self._lock:
            self._target_progress = 0.0
            self._display_progress = 0.0
            self._start_time = time.time()
            self._last_update_time = time.time()
            self._last_render_time = time.time()
            self._render()
    
    def finish(self) -> None:
        """Finish the progress bar at 100%."""
        with self._lock:
            self._target_progress = 1.0
            self._display_progress = 1.0
            self._render()
            self._animation_running = False

class ConsoleProgressBar(SmoothProgressBar):
    """
    A console-based progress bar implementation.
    
    This progress bar renders to the console using ANSI escape codes for a
    smooth, fluid animation.
    """
    
    def __init__(
        self,
        config: Optional[ProgressBarConfig] = None,
        stream=None
    ):
        """
        Initialize the console progress bar.
        
        Args:
            config: Configuration for the progress bar
            stream: Stream to write to (defaults to sys.stdout)
        """
        import sys
        super().__init__(config)
        self.stream = stream or sys.stdout
        self._last_line_length = 0
    
    def _render(self) -> None:
        """Render the progress bar to the console."""
        # Calculate filled width
        filled_width = int(self._display_progress * self.config.width)
        empty_width = self.config.width - filled_width
        
        # Build the progress bar string
        progress_bar = self.config.fill_char * filled_width + self.config.empty_char * empty_width
        
        # Add percentage if enabled
        if self.config.show_percentage:
            percentage = int(self._display_progress * 100)
            progress_bar = f"{progress_bar} {percentage}%"
        
        # Add elapsed time if enabled
        if self.config.show_elapsed_time:
            elapsed = int(time.time() - self._start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            progress_bar = f"{progress_bar} [{time_str}]"
        
        # Clear the previous line and write the new one
        self.stream.write("\r" + " " * self._last_line_length + "\r")
        self.stream.write(progress_bar)
        self.stream.flush()
        
        # Update the last line length
        self._last_line_length = len(progress_bar)
    
    def finish(self) -> None:
        """Finish the progress bar at 100% and move to the next line."""
        super().finish()
        self.stream.write("\n")
        self.stream.flush() 