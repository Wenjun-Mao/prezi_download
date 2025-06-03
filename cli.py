"""Command-line interface for the Prezi downloader."""

import argparse
import sys
from pathlib import Path

from utils.prezi_scraper import PreziScraper
from utils.config import ScraperConfig


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Download screenshots and YouTube links from Prezi presentations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py https://prezi.com/p/example-presentation/
  python cli.py https://prezi.com/p/example/ --output my_output --headless false
  python cli.py https://prezi.com/p/example/ --max-slides 20 --delay 3
        """
    )
    
    parser.add_argument(
        'url',
        help='Prezi presentation URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='prezi_output',
        help='Output directory (default: prezi_output)'
    )
    
    parser.add_argument(
        '--headless',
        type=str,
        choices=['true', 'false'],
        default='true',
        help='Run browser in headless mode (default: true)'
    )
    
    parser.add_argument(
        '--max-slides',
        type=int,
        default=50,
        help='Maximum number of slides to capture (default: 50)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between screenshots in seconds (default: 2.0)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Page load timeout in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--window-size',
        default='1920x1080',
        help='Browser window size (default: 1920x1080)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser


def validate_url(url: str) -> bool:
    """Validate that the URL is a Prezi URL."""
    if not url:
        return False
    
    url_lower = url.lower()
    return 'prezi.com' in url_lower and '/p/' in url_lower


def parse_window_size(size_str: str) -> tuple[int, int]:
    """Parse window size string like '1920x1080' into width, height."""
    try:
        width, height = size_str.split('x')
        return int(width), int(height)
    except (ValueError, AttributeError):
        print(f"Invalid window size format: {size_str}. Using default 1920x1080")
        return 1920, 1080


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate URL
    if not validate_url(args.url):
        print(f"Error: Invalid Prezi URL: {args.url}")
        print("Prezi URLs should look like: https://prezi.com/p/presentation-name/")
        sys.exit(1)
    
    # Parse window size
    width, height = parse_window_size(args.window_size)
    
    # Create configuration
    config = ScraperConfig(
        output_dir=args.output,
        headless=args.headless.lower() == 'true',
                window_width=width,
        window_height=height,
        page_load_timeout=args.timeout,
        screenshot_delay=args.delay,
        max_slides=args.max_slides,
    )
    
    if args.verbose:
        print("Configuration:")
        print(f"  URL: {args.url}")
        print(f"  Output: {config.output_dir}")
        print(f"  Headless: {config.headless}")
        print(f"  Window: {config.window_width}x{config.window_height}")
        print(f"  Max slides: {config.max_slides}")
        print(f"  Screenshot delay: {config.screenshot_delay}s")
        print()
    
    # Initialize scraper
    scraper = PreziScraper(
        output_dir=config.output_dir,
        headless=config.headless
    )
    
    try:
        print(f"Starting Prezi scrape: {args.url}")
        results = scraper.scrape_prezi(args.url)
        
        # Print results
        print("\n" + "="*60)
        print("SCRAPING COMPLETED")
        print("="*60)
        print(f"Presentation: {results['title']}")
        print(f"Screenshots captured: {len(results['screenshots'])}")
        print(f"YouTube links found: {len(results['youtube_links'])}")
        
        if results['screenshots']:
            print(f"\nScreenshots saved to: {config.get_screenshots_path()}")
            if args.verbose:
                for screenshot in results['screenshots']:
                    print(f"  - {Path(screenshot).name}")
        
        if results['youtube_links']:
            youtube_file = scraper.youtube_extractor.save_links_to_file()
            print(f"YouTube links saved to: {youtube_file}")
            if args.verbose:
                for link in results['youtube_links']:
                    print(f"  - {link}")
        
        print(f"\nAll output saved to: {Path(config.output_dir).absolute()}")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during scraping: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
