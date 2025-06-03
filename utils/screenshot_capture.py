"""Screenshot capture utility for taking screenshots of web pages."""

import time
from pathlib import Path
from typing import Optional
from datetime import datetime

from selenium.webdriver.common.by import By


class ScreenshotCapture:
    """Utility class for capturing screenshots."""
    
    def __init__(self, output_dir: str):
        """
        Initialize screenshot capture utility.
        
        Args:
            output_dir: Directory to save screenshots
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def capture_full_page(self, driver, filename: str) -> Optional[str]:
        """
        Capture a full-page screenshot.
        
        Args:
            driver: Selenium WebDriver instance
            filename: Base filename for the screenshot (without extension)
            
        Returns:
            Path to the saved screenshot or None if failed
        """
        try:            # Get the full page height
            total_height = driver.execute_script("return document.body.scrollHeight")
            
            # Set window size to capture full content
            driver.set_window_size(1920, max(1080, total_height))
            
            # Wait a moment for any dynamic content to load
            time.sleep(1)
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{filename}_{timestamp}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            if driver.save_screenshot(str(screenshot_path)):
                print(f"Screenshot saved: {screenshot_path}")
                return str(screenshot_path)
            else:
                print(f"Failed to save screenshot: {screenshot_path}")
                return None
                
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
    
    def capture_element(self, driver, element_selector: str, filename: str) -> Optional[str]:
        """
        Capture a screenshot of a specific element.
        
        Args:
            driver: Selenium WebDriver instance
            element_selector: CSS selector for the element to capture
            filename: Base filename for the screenshot
            
        Returns:
            Path to the saved screenshot or None if failed
        """
        try:
            element = driver.find_element(By.CSS_SELECTOR, element_selector)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{filename}_{timestamp}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            if element.screenshot(str(screenshot_path)):
                print(f"Element screenshot saved: {screenshot_path}")
                return str(screenshot_path)
            else:
                print(f"Failed to save element screenshot: {screenshot_path}")
                return None
                
        except Exception as e:
            print(f"Error capturing element screenshot: {e}")
            return None
    
    def capture_viewport(self, driver, filename: str) -> Optional[str]:
        """
        Capture a screenshot of the current viewport.
        
        Args:
            driver: Selenium WebDriver instance
            filename: Base filename for the screenshot
            
        Returns:
            Path to the saved screenshot or None if failed
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{filename}_{timestamp}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            if driver.save_screenshot(str(screenshot_path)):
                print(f"Viewport screenshot saved: {screenshot_path}")
                return str(screenshot_path)
            else:
                print(f"Failed to save viewport screenshot: {screenshot_path}")
                return None
                
        except Exception as e:
            print(f"Error capturing viewport screenshot: {e}")
            return None
