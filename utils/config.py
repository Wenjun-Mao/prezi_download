"""Configuration settings for the Prezi downloader."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScraperConfig:
    """Configuration for the Prezi scraper."""
    
    # Output settings
    output_dir: str = "prezi_output"
    screenshots_dir: str = "screenshots"
    
    # Browser settings
    headless: bool = True
    window_width: int = 1920
    window_height: int = 1080
    
    # Timing settings
    page_load_timeout: int = 30
    element_wait_timeout: int = 10
    screenshot_delay: float = 2.0
    navigation_delay: float = 1.5
    
    # Navigation settings
    max_slides: int = 50  # Prevent infinite loops
    retry_attempts: int = 3
    
    # Output settings
    screenshot_format: str = "png"
    screenshot_quality: int = 95
    
    # YouTube extraction settings
    save_youtube_links: bool = True
    youtube_filename: str = "youtube_links.txt"
    
    @classmethod
    def from_env(cls) -> 'ScraperConfig':
        """Create config from environment variables."""
        return cls(
            output_dir=os.getenv('PREZI_OUTPUT_DIR', cls.output_dir),
            headless=os.getenv('PREZI_HEADLESS', 'true').lower() == 'true',
            window_width=int(os.getenv('PREZI_WINDOW_WIDTH', cls.window_width)),
            window_height=int(os.getenv('PREZI_WINDOW_HEIGHT', cls.window_height)),
            page_load_timeout=int(os.getenv('PREZI_PAGE_TIMEOUT', cls.page_load_timeout)),
            max_slides=int(os.getenv('PREZI_MAX_SLIDES', cls.max_slides)),
        )
    
    def get_output_path(self) -> Path:
        """Get the absolute path to the output directory."""
        return Path(self.output_dir).resolve()
    
    def get_screenshots_path(self) -> Path:
        """Get the absolute path to the screenshots directory."""
        return self.get_output_path() / self.screenshots_dir
    
    def ensure_directories(self) -> None:
        """Ensure output directories exist."""
        self.get_output_path().mkdir(exist_ok=True)
        self.get_screenshots_path().mkdir(exist_ok=True)
