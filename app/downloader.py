"""Core downloader module."""
import os
import requests
from app.config import OUTPUT_DIR, REQUEST_TIMEOUT, USER_AGENT
from app.utils import sanitize_filename, get_unique_filepath


class Downloader:
    """Handles downloading media files."""

    def __init__(self, output_dir: str = OUTPUT_DIR):
        """Initialize the downloader.

        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_url(self, url: str, filename: str, extension: str = ".mp4") -> str:
        """Download a file from a URL.

        Args:
            url: The URL to download from
            filename: The desired filename (will be sanitized)
            extension: The file extension

        Returns:
            The path to the downloaded file

        Raises:
            Exception: If download fails
        """
        try:
            filename = sanitize_filename(filename)
            filepath = get_unique_filepath(self.output_dir, filename, extension)

            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            response.raise_for_status()

            # Download in chunks
            total_size = 0
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)

            print(f"✓ Downloaded: {filepath} ({total_size / (1024*1024):.2f} MB)")
            return filepath

        except requests.exceptions.RequestException as e:
            raise Exception(f"Download failed: {str(e)}")
        except IOError as e:
            raise Exception(f"File write error: {str(e)}")
