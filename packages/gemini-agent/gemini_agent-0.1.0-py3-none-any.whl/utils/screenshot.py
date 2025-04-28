import io
import platform
import pyautogui
from typing import Tuple, Optional, Union


class ScreenshotManager:
    """
    Utility for capturing and managing screenshots.
    """
    
    def __init__(self):
        """Initialize the screenshot manager."""
        self.current_platform = platform.system().lower()
        
    def capture_screenshot(self) -> bytes:
        """
        Capture a screenshot of the current screen.
        
        Returns:
            Screenshot as bytes
        """
        # Capture screenshot using pyautogui
        screenshot = pyautogui.screenshot()
        
        # Convert to bytes
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        return buffer.getvalue()
    
    def get_screen_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions of the current screen.
        
        Returns:
            Tuple of (width, height)
        """
        screen_width, screen_height = pyautogui.size()
        return screen_width, screen_height