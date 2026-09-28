# Social Media Video Downloader

A minimal Python CLI tool to download single videos from **TikTok**, **Instagram**, and **YouTube**.

## Features

✅ Download single videos from:
  - YouTube
  - Instagram (reels, posts, stories)
  - TikTok

✅ Automatic platform detection
✅ High-quality video downloads
✅ Sanitized filenames
✅ Duplicate file handling
✅ Simple CLI interface

## Installation

### Prerequisites
- Python 3.8+
- pip
- ffmpeg (optional, recommended for better format support)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jull360/social-media-video-downloader.git
cd social-media-video-downloader
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (optional):
```bash
cp .env.example .env
```

## Usage

### Download a YouTube video:
```bash
python -m app.main --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Download an Instagram reel/post:
```bash
python -m app.main --url "https://www.instagram.com/reel/ABC123XYZ/"
```

### Download a TikTok video:
```bash
python -m app.main --url "https://www.tiktok.com/@username/video/1234567890123456789"
```

### Short form:
```bash
python -m app.main -u "<URL>"
```

## Output

Downloaded videos are saved to the `output/` directory with sanitized filenames.

## Configuration

Edit `.env` to customize:

```env
OUTPUT_DIR=./output           # Where to save videos
USER_AGENT=...                # Custom User-Agent header
REQUEST_TIMEOUT=10            # Request timeout in seconds
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                # CLI entry point
│   ├── config.py              # Configuration
│   ├── models.py              # Data models
│   ├── utils.py               # Utility functions
│   ├── downloader.py          # Core downloader
│   └── providers/
│       ├── __init__.py
│       ├── youtube.py         # YouTube provider
│       ├── instagram.py       # Instagram provider
│       └── tiktok.py          # TikTok provider
├── output/                    # Downloaded videos (created on first run)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How It Works

1. **Platform Detection**: Analyzes the URL to detect the source platform
2. **Media Extraction**: Uses platform-specific methods to extract video metadata
3. **URL Extraction**: Finds the direct media download URL
4. **Download**: Fetches the video file and saves it locally
5. **Post-processing**: Sanitizes filename and handles duplicates

### Providers

- **YouTube**: Uses `yt-dlp` for reliable video extraction and downloading
- **Instagram**: Extracts video URLs from HTML metadata
- **TikTok**: Parses page content to find downloadable video URLs

## Limitations

- **Single videos only** (no playlists)
- **Public content only** (no login/auth required)
- **TikTok/Instagram** may break if the platforms change their HTML structure
- **Instagram Stories** may not work reliably
- Downloads may include platform watermarks

## Legal Notice

⚠️ **Important**: Only download content you own or have permission to download. Respect copyright and platform terms of service.

## Troubleshooting

### YouTube videos not downloading?
- Ensure `yt-dlp` is up to date: `pip install --upgrade yt-dlp`
- Some videos may be region-restricted or age-restricted

### Instagram/TikTok downloads failing?
- The platforms may have changed their page structure
- Ensure you're using a public post URL
- Private accounts/posts cannot be downloaded

### File permission errors?
- Ensure the `output/` directory is writable
- Check that your user has write permissions

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for educational purposes. Users are responsible for complying with platform terms of service and applicable laws regarding content downloading.
