"""YouTube link extraction utility."""

import re
from pathlib import Path
from typing import Set, List
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class YouTubeExtractor:
    """Utility class for extracting YouTube links from web content."""
    
    def __init__(self, output_dir: str):
        """
        Initialize YouTube extractor.
        
        Args:
            output_dir: Directory to save extracted links
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.youtube_links: Set[str] = set()
        self.link_details: List[dict] = []
    
    def extract_youtube_link(self, url: str) -> bool:
        """
        Extract and process a YouTube link.
        
        Args:
            url: URL that might contain YouTube content
            
        Returns:
            True if a valid YouTube link was found and processed
        """
        youtube_url = self._normalize_youtube_url(url)
        if youtube_url and youtube_url not in self.youtube_links:
            self.youtube_links.add(youtube_url)
            
            # Extract video details
            video_id = self._extract_video_id(youtube_url)
            details = {
                'url': youtube_url,
                'video_id': video_id,
                'extracted_at': datetime.now().isoformat(),
                'source': 'iframe'
            }
            self.link_details.append(details)
            
            print(f"Found YouTube link: {youtube_url}")
            return True
        return False
    
    def extract_from_page_source(self, page_source: str) -> int:
        """
        Extract YouTube links from page source.
        
        Args:
            page_source: HTML source code of the page
            
        Returns:
            Number of new YouTube links found
        """
        initial_count = len(self.youtube_links)
        
        # Patterns to match YouTube URLs
        patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
            r'https?://youtu\.be/([a-zA-Z0-9_-]+)',
            r'https?://(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, page_source, re.IGNORECASE)
            for match in matches:
                youtube_url = match.group(0)
                normalized_url = self._normalize_youtube_url(youtube_url)
                
                if normalized_url and normalized_url not in self.youtube_links:
                    self.youtube_links.add(normalized_url)
                    
                    video_id = match.group(1)
                    details = {
                        'url': normalized_url,
                        'video_id': video_id,
                        'extracted_at': datetime.now().isoformat(),
                        'source': 'page_source'
                    }
                    self.link_details.append(details)
                    
                    print(f"Found YouTube link in source: {normalized_url}")
        
        return len(self.youtube_links) - initial_count
    
    def _normalize_youtube_url(self, url: str) -> str:
        """
        Normalize a YouTube URL to a standard format.
        
        Args:
            url: Raw URL that might be a YouTube link
            
        Returns:
            Normalized YouTube URL or empty string if not a valid YouTube URL
        """
        if not url:
            return ""
        
        # Parse the URL
        parsed = urlparse(url)
        
        # Check if it's a YouTube domain
        if parsed.netloc not in ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']:
            return ""
        
        # Extract video ID based on URL format
        video_id = None
        
        if 'youtu.be' in parsed.netloc:
            # Short format: https://youtu.be/VIDEO_ID
            video_id = parsed.path.lstrip('/')
        elif 'youtube.com' in parsed.netloc:
            if '/watch' in parsed.path:
                # Standard format: https://youtube.com/watch?v=VIDEO_ID
                query_params = parse_qs(parsed.query)
                video_id = query_params.get('v', [None])[0]
            elif '/embed/' in parsed.path:
                # Embed format: https://youtube.com/embed/VIDEO_ID
                video_id = parsed.path.split('/embed/')[-1].split('?')[0]
            elif '/v/' in parsed.path:
                # Old format: https://youtube.com/v/VIDEO_ID
                video_id = parsed.path.split('/v/')[-1].split('?')[0]
        
        if video_id and self._is_valid_video_id(video_id):
            return f"https://www.youtube.com/watch?v={video_id}"
        
        return ""
    
    def _extract_video_id(self, youtube_url: str) -> str:
        """
        Extract video ID from a normalized YouTube URL.
        
        Args:
            youtube_url: Normalized YouTube URL
            
        Returns:
            Video ID or empty string if not found
        """
        parsed = urlparse(youtube_url)
        query_params = parse_qs(parsed.query)
        return query_params.get('v', [''])[0]
    
    def _is_valid_video_id(self, video_id: str) -> bool:
        """
        Check if a video ID is valid.
        
        Args:
            video_id: YouTube video ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not video_id:
            return False
        
        # YouTube video IDs are typically 11 characters long
        # and contain alphanumeric characters, hyphens, and underscores
        return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))
    
    def get_extracted_links(self) -> List[str]:
        """
        Get all extracted YouTube links.
        
        Returns:
            List of extracted YouTube URLs
        """
        return list(self.youtube_links)
    
    def save_links_to_file(self, filename: str = None) -> str:
        """
        Save extracted YouTube links to a text file.
        
        Args:
            filename: Custom filename (optional)
            
        Returns:
            Path to the saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_links_{timestamp}.txt"
        
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Extracted YouTube Links\n")
            f.write("=" * 50 + "\n\n")
            
            if not self.youtube_links:
                f.write("No YouTube links found.\n")
            else:
                for i, link in enumerate(sorted(self.youtube_links), 1):
                    f.write(f"{i}. {link}\n")
                
                f.write(f"\nTotal links found: {len(self.youtube_links)}\n")
                
                # Add detailed information
                f.write("\n" + "=" * 50 + "\n")
                f.write("Detailed Information\n")
                f.write("=" * 50 + "\n\n")
                
                for details in self.link_details:
                    f.write(f"URL: {details['url']}\n")
                    f.write(f"Video ID: {details['video_id']}\n")
                    f.write(f"Source: {details['source']}\n")
                    f.write(f"Extracted at: {details['extracted_at']}\n")
                    f.write("-" * 30 + "\n")
        
        print(f"YouTube links saved to: {file_path}")
        return str(file_path)
    
    def clear_links(self):
        """Clear all extracted links."""
        self.youtube_links.clear()
        self.link_details.clear()
