"""Interactive CLI selection with cross-platform support"""

from typing import List, Optional
from prompt_toolkit.shortcuts import radiolist_dialog
from ..utils.logger import log

class InteractiveSelector:
    """Handles arrow-key selection from a list of items"""
    
    def __init__(self, items: List[str], prompt: str = "Select an option:"):
        self.items = items
        self.prompt = prompt
        self.max_display = 3  # Show max 3 items
        
    def select(self) -> Optional[str]:
        """Run interactive selection, return chosen item or None if cancelled"""
        try:
            # Limit to max 3 items for display
            display_items = self.items[:self.max_display]
            
            # Format for radiolist
            choices = [(item, item) for item in display_items]
            
            # Run dialog with consistent styling
            result = radiolist_dialog(
                title=self.prompt,
                text="Use ↑↓ to navigate, Enter to select, Ctrl+C to cancel",
                values=choices,
                style={
                    "dialog": "bg:#222222",
                    "dialog.body": "bg:#000000",
                    "dialog.shadow": "bg:#222222",
                }
            ).run()
            
            return result  # None if cancelled
            
        except KeyboardInterrupt:
            print("\nCancelled")
            return None
        except Exception as e:
            log.error(f"Selection failed: {e}")
            return None 