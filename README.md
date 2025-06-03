# Prezi Downloader

A modular Python project for downloading content from Prezi presentations, including screenshot capture and YouTube link extraction.

## Features

- **Screenshot Capture**: Take full-page screenshots of Prezi slides
- **YouTube Link Extraction**: Extract and save YouTube video links found in presentations
- **Modular Design**: Separate utilities that can be used independently
- **Automated Navigation**: Attempts to navigate through Prezi presentations automatically

## Project Structure

```
prezi_download/
├── utils/
│   ├── __init__.py
│   ├── prezi_scraper.py      # Main scraper coordinator
│   ├── screenshot_capture.py # Screenshot utilities
│   └── youtube_extractor.py  # YouTube link extraction
├── main.py                   # Example usage script
├── mybook.ipynb             # Jupyter notebook with examples
└── pyproject.toml           # Project dependencies
```

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   uv sync
   # or
   pip install -e .
   ```

3. **Install ChromeDriver**:
   - Download ChromeDriver matching your Chrome browser version
   - Ensure it's in your PATH or system can find it

## Usage

### Quick Start

Run the main script:
```bash
python main.py
```

Enter a Prezi URL when prompted, and the script will:
1. Navigate through the presentation
2. Capture screenshots of slides
3. Extract any YouTube links found
4. Save everything to organized output folders

### Using Individual Utilities

Each utility can be used independently:

```python
# Just screenshot capture
from utils.screenshot_capture import ScreenshotCapture
screenshot_util = ScreenshotCapture("output")

# Just YouTube extraction
from utils.youtube_extractor import YouTubeExtractor
youtube_util = YouTubeExtractor("output")

# Full Prezi scraping
from utils.prezi_scraper import PreziScraper
scraper = PreziScraper("output")
```

### Jupyter Notebook

Open `mybook.ipynb` for interactive examples and detailed demonstrations of each utility.

## Output Structure

The scraper creates organized output:
```
prezi_output/
├── screenshots/
│   ├── slide_001_20250602_143022.png
│   ├── slide_002_20250602_143025.png
│   └── ...
└── youtube_links_20250602_143030.txt
```

## Requirements

- Python 3.12+
- Chrome browser
- ChromeDriver (matching Chrome version)
- Dependencies listed in `pyproject.toml`

## Supported Prezi URL Formats

- `https://prezi.com/p/presentation-name/`
- `https://www.prezi.com/p/presentation-name/`

## Limitations

- Requires public Prezi presentations (no login support yet)
- Navigation depends on Prezi's current UI structure
- Some dynamic content may not be captured perfectly
- Rate limiting may apply for extensive scraping

## Customization

- **Screenshot settings**: Modify `ScreenshotCapture` class
- **YouTube patterns**: Adjust regex patterns in `YouTubeExtractor`
- **Navigation logic**: Customize slide navigation in `PreziScraper`
- **Output formats**: Extend utilities to support additional formats

## Troubleshooting

- **ChromeDriver issues**: Ensure ChromeDriver version matches Chrome browser
- **Prezi access**: Verify the presentation is publicly accessible
- **Navigation failures**: Some Prezi presentations may have complex navigation that requires manual adjustment
- **Empty results**: Check if the presentation contains the expected content types

## Contributing

Feel free to extend the utilities for:
- Additional presentation platforms
- More embedded content types (Vimeo, etc.)
- Better navigation algorithms
- OCR for text extraction
- Audio/video content detection

## License

This project is for educational and personal use. Respect Prezi's terms of service and content creators' rights when using this tool.