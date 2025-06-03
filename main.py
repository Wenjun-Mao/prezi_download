"""
Main script demonstrating how to use the Prezi downloading utilities.

This script shows how to:
1. Scrape a Prezi presentation
2. Take screenshots of slides  
3. Extract YouTube links
4. Save results to organized files
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import PreziScraper


def main():
    """Main function to demonstrate Prezi scraping."""
    
    # Example Prezi URL - replace with actual URL
    prezi_url = input("Enter Prezi URL: ").strip()
    
    if not prezi_url:
        print("No URL provided. Using example URL for demonstration.")
        prezi_url = "https://prezi.com/p/example-presentation/"
    
    # Create output directory
    output_dir = "prezi_output"
    
    # Initialize the scraper
    print("Initializing Prezi scraper...")
    scraper = PreziScraper(output_dir=output_dir, headless=True)
    
    try:
        # Scrape the presentation
        print(f"Scraping Prezi presentation: {prezi_url}")
        results = scraper.scrape_prezi(prezi_url)
        
        # Print results summary
        print("\n" + "="*50)
        print("SCRAPING RESULTS")
        print("="*50)
        print(f"Presentation title: {results['title']}")
        print(f"Screenshots captured: {len(results['screenshots'])}")
        print(f"YouTube links found: {len(results['youtube_links'])}")
        
        # List screenshots
        if results['screenshots']:
            print("\nScreenshots saved:")
            for i, screenshot in enumerate(results['screenshots'], 1):
                print(f"  {i}. {screenshot}")
        
        # List YouTube links
        if results['youtube_links']:
            print("\nYouTube links found:")
            for i, link in enumerate(results['youtube_links'], 1):
                print(f"  {i}. {link}")
            
            # Save YouTube links to file
            youtube_file = scraper.youtube_extractor.save_links_to_file()
            print(f"\nYouTube links saved to: {youtube_file}")
        
        print(f"\nAll output saved to: {os.path.abspath(output_dir)}")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
