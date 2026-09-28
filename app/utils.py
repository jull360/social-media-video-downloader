"""Utility functions."""
import re
import os
from urllib.parse import urlparse
from app.config import PLATFORMS


def detect_platform(url: str) -> str:
    """Detect the platform from a URL.

    Args:
        url: The media URL

    Returns:
        The platform name (youtube, instagram, tiktok) or 'unknown'
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")

    for platform, domains in PLATFORMS.items():
        for d in domains:
            if d in domain:
                return platform

    return "unknown"


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """Sanitize a filename to be filesystem-safe.

    Args:
        filename: The filename to sanitize
        max_length: Maximum length of the filename

    Returns:
        A sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces/underscores with single
    filename = re.sub(r'[\s_]+', '_', filename)
    # Limit length
    filename = filename[:max_length]
    # Remove trailing dots and spaces
    filename = filename.rstrip('. ')
    return filename if filename else "video"


def get_unique_filepath(directory: str, filename: str, extension: str) -> str:
    """Get a unique filepath by appending a number if the file already exists.

    Args:
        directory: The directory path
        filename: The base filename without extension
        extension: The file extension (e.g., '.mp4')

    Returns:
        A unique filepath
    """
    filepath = os.path.join(directory, f"{filename}{extension}")

    if not os.path.exists(filepath):
        return filepath

    counter = 1
    while True:
        filepath = os.path.join(directory, f"{filename}_{counter}{extension}")
        if not os.path.exists(filepath):
            return filepath
        counter += 1
