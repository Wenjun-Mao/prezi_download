"""Test script for debugging YouTube URL extraction."""

import sys
from pathlib import Path
from urllib.parse import urlparse

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.youtube_extractor import YouTubeExtractor

def debug_youtube_extraction():
    """Debug YouTube URL extraction step by step."""
    print("Debugging YouTube URL extraction...")
    print("=" * 50)
    
    extractor = YouTubeExtractor("debug_output")
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ", 
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://example.com/not-youtube",
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing URL: {url}")
        
        # Parse URL
        parsed = urlparse(url)
        print(f"   Parsed netloc: '{parsed.netloc}'")
        print(f"   Parsed path: '{parsed.path}'")
        print(f"   Parsed query: '{parsed.query}'")
        
        # Test normalization
        normalized = extractor._normalize_youtube_url(url)
        print(f"   Normalized: '{normalized}'")
        
        # Test extraction
        result = extractor.extract_youtube_link(url)
        print(f"   Extraction result: {result}")
    
    print(f"\nFinal extracted links: {extractor.get_extracted_links()}")

if __name__ == "__main__":
    debug_youtube_extraction()
