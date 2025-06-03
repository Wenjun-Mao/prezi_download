"""Main Prezi scraper module that coordinates screenshot capture and YouTube link extraction."""

import time
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .screenshot_capture import ScreenshotCapture
from .youtube_extractor import YouTubeExtractor


class PreziScraper:
    """Main class for scraping Prezi presentations."""
    
    def __init__(self, output_dir: str = "prezi_output", headless: bool = True):
        """
        Initialize the Prezi scraper.
        
        Args:
            output_dir: Directory to save output files
            headless: Whether to run browser in headless mode
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.screenshots_dir = self.output_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        
        self.screenshot_capture = ScreenshotCapture(str(self.screenshots_dir))
        self.youtube_extractor = YouTubeExtractor(str(self.output_dir))
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver with appropriate options."""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        return webdriver.Chrome(options=options)
    
    def scrape_prezi(self, prezi_url: str) -> Dict[str, List[str]]:
        """
        Scrape a Prezi presentation.
        
        Args:
            prezi_url: URL of the Prezi presentation
            
        Returns:
            Dictionary with lists of screenshot paths and YouTube links
        """
        if not self._is_valid_prezi_url(prezi_url):
            raise ValueError("Invalid Prezi URL provided")
        
        self.driver = self._setup_driver()
        
        try:
            print(f"Loading Prezi: {prezi_url}")
            self.driver.get(prezi_url)
            
            # Wait for the presentation to load
            self._wait_for_prezi_load()
            
            # Extract presentation info
            presentation_title = self._get_presentation_title()
            print(f"Processing presentation: {presentation_title}")
            
            # Process slides
            screenshots = self._process_slides()
            youtube_links = self.youtube_extractor.get_extracted_links()
            
            return {
                "screenshots": screenshots,
                "youtube_links": youtube_links,
                "title": presentation_title
            }
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def _is_valid_prezi_url(self, url: str) -> bool:
        """Check if the URL is a valid Prezi URL."""
        parsed = urlparse(url)
        return parsed.netloc in ['prezi.com', 'www.prezi.com'] and '/p/' in parsed.path
    
    def _wait_for_prezi_load(self, timeout: int = 30):
        """Wait for Prezi presentation to fully load."""
        try:
            # Wait for the presentation viewer to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "presentation-viewer"))
            )
            
            # Additional wait for content to render
            time.sleep(5)
            
        except TimeoutException:
            print("Warning: Prezi presentation may not have loaded completely")
    
    def _get_presentation_title(self) -> str:
        """Extract the presentation title."""
        try:
            title_element = self.driver.find_element(By.TAG_NAME, "title")
            title = title_element.get_attribute("textContent") or "untitled_prezi"
            # Clean title for use as filename
            return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        except NoSuchElementException:
            return "untitled_prezi"
    
    def _process_slides(self) -> List[str]:
        """Process all slides in the presentation."""
        screenshots = []
        slide_count = 0
        
        # Try to find navigation elements or slides
        try:
            # Look for slide navigation or frames
            self._navigate_through_slides(screenshots, slide_count)
            
        except Exception as e:
            print(f"Error processing slides: {e}")            # Fallback: take a screenshot of the current view
            screenshot_path = self.screenshot_capture.capture_full_page(
                self.driver, "slide_001"
            )
            if screenshot_path:
                screenshots.append(screenshot_path)
        
        return screenshots
    
    def _navigate_through_slides(self, screenshots: List[str], slide_count: int):
        """Navigate through slides and capture screenshots."""
        # This is a simplified approach - Prezi navigation can be complex
        # We'll capture the main view and any embedded content
        
        # Capture main presentation view
        screenshot_path = self.screenshot_capture.capture_full_page(
            self.driver, f"slide_{slide_count + 1:03d}"
        )
        if screenshot_path:
            screenshots.append(screenshot_path)
            slide_count += 1
        
        # Look for YouTube iframes and process them
        self._process_embedded_content()
        
        # Try to find and click through navigation elements
        nav_elements = self.driver.find_elements(By.CSS_SELECTOR, 
            "[class*='nav'], [class*='next'], [class*='arrow'], [data-testid*='nav']")
        
        for nav_element in nav_elements[:10]:  # Limit to prevent infinite loops
            try:
                if nav_element.is_displayed() and nav_element.is_enabled():
                    nav_element.click()
                    time.sleep(2)  # Wait for transition
                    
                    screenshot_path = self.screenshot_capture.capture_full_page(
                        self.driver, f"slide_{slide_count + 1:03d}"
                    )
                    if screenshot_path:
                        screenshots.append(screenshot_path)
                        slide_count += 1
                    
                    self._process_embedded_content()
                    
            except Exception as e:
                print(f"Error clicking navigation element: {e}")
                continue
    
    def _process_embedded_content(self):
        """Process embedded content like YouTube videos."""
        # Find YouTube iframes
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            try:
                src = iframe.get_attribute("src")
                if src and "youtube" in src:
                    self.youtube_extractor.extract_youtube_link(src)
            except Exception as e:
                print(f"Error processing iframe: {e}")
        
        # Also look for YouTube links in the page source
        page_source = self.driver.page_source
        self.youtube_extractor.extract_from_page_source(page_source)
