"""Test script to verify that all utilities are working correctly."""

import sys
import shutil
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from utils import PreziScraper, ScreenshotCapture, YouTubeExtractor, ScraperConfig
        print("✅ All utilities imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_config():
    """Test configuration module."""
    print("\nTesting configuration...")
    
    try:
        from utils.config import ScraperConfig
        
        # Test default config
        config = ScraperConfig()
        
        # Test environment config
        env_config = ScraperConfig.from_env()
        
        # Test path methods
        output_path = config.get_output_path()
        screenshots_path = config.get_screenshots_path()
        
        print("✅ Configuration module working correctly")
        print(f"   Default output: {output_path}")
        print(f"   Screenshots path: {screenshots_path}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_youtube_extractor():
    """Test YouTube link extraction functionality."""
    print("\nTesting YouTube extractor...")
    
    try:
        from utils.youtube_extractor import YouTubeExtractor
        
        # Create temporary extractor
        extractor = YouTubeExtractor("test_output")
        
        # Test URLs
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "https://example.com/not-youtube",  # Should be ignored
        ]
        
        valid_count = 0
        for url in test_urls:
            if extractor.extract_youtube_link(url):
                valid_count += 1
        
        extracted_links = extractor.get_extracted_links()
        
        if valid_count == 3 and len(extracted_links) == 1:  # 3 valid URLs, 1 unique link
            print("✅ YouTube extractor working correctly")
            print(f"   Processed {valid_count} valid URLs, extracted {len(extracted_links)} unique link(s)")
            for link in extracted_links:
                print(f"   - {link}")
            return True
        else:
            print(f"❌ YouTube extractor test failed")
            print(f"   Expected 3 valid URLs and 1 unique link")
            print(f"   Got {valid_count} valid URLs and {len(extracted_links)} unique links")
            return False
            
    except Exception as e:
        print(f"❌ YouTube extractor error: {e}")
        return False


def test_screenshot_capture():
    """Test screenshot capture utility."""
    print("\nTesting screenshot capture...")
    
    try:
        from utils.screenshot_capture import ScreenshotCapture
        
        # Create temporary capture utility
        capture = ScreenshotCapture("test_screenshots")
        
        # Check if output directory was created
        if capture.output_dir.exists():
            print("✅ Screenshot capture utility initialized correctly")
            print(f"   Output directory: {capture.output_dir}")
            return True
        else:
            print("❌ Screenshot capture directory not created")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot capture error: {e}")
        return False


def test_prezi_scraper_init():
    """Test Prezi scraper initialization (without actually scraping)."""
    print("\nTesting Prezi scraper initialization...")
    
    try:
        from utils.prezi_scraper import PreziScraper
        
        # Test initialization without starting browser
        scraper = PreziScraper(output_dir="test_prezi_output", headless=True)
        
        # Check if directories were created
        if scraper.output_dir.exists() and scraper.screenshots_dir.exists():
            print("✅ Prezi scraper initialized correctly")
            print(f"   Output directory: {scraper.output_dir}")
            print(f"   Screenshots directory: {scraper.screenshots_dir}")
            return True
        else:
            print("❌ Prezi scraper directories not created")
            return False
            
    except Exception as e:
        print(f"❌ Prezi scraper error: {e}")
        return False


def cleanup_test_directories():
    """Clean up test directories created during testing."""
    print("\nCleaning up test directories...")
    
    test_dirs = [
        "test_output",
        "test_screenshots", 
        "test_prezi_output"
    ]
    
    for test_dir in test_dirs:
        dir_path = Path(test_dir)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed: {test_dir}")


def main():
    """Run all tests."""
    print("Prezi Downloader - Utility Tests")
    print("=" * 40)
    
    # Run tests
    tests = [
        test_imports,
        test_config,
        test_youtube_extractor,
        test_screenshot_capture,
        test_prezi_scraper_init
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    # Clean up
    cleanup_test_directories()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
