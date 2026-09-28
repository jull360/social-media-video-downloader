"""TikTok provider."""
import re
import requests
from app.models import MediaInfo
from app.config import USER_AGENT, REQUEST_TIMEOUT


class TikTokProvider:
    """Handles TikTok video downloads."""

    @staticmethod
    def extract_media_url(url: str) -> str:
        """Extract direct media URL from TikTok post.

        Args:
            url: TikTok URL

        Returns:
            Direct media URL

        Raises:
            Exception: If extraction fails
        """
        try:
            # TikTok URLs with watermark can sometimes be fetched directly
            # We'll try to get the HTML and extract embedded data
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            response.raise_for_status()

            html = response.text

            # Look for video URL in various locations in the HTML
            patterns = [
                r'"downloadAddr":"([^"]+)"',
                r'"playAddr":"([^"]+)"',
                r'"video_download_url":"([^"]+)"',
                r'og:video.*?content="([^"]+)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    media_url = match.group(1)
                    # Unescape the URL
                    media_url = media_url.replace("\\/", "/")
                    # TikTok URLs often have parameters that need to be kept
                    if media_url.startswith("http"):
                        return media_url

            raise Exception("Could not find video URL in TikTok post")

        except requests.exceptions.RequestException as e:
            raise Exception(f"TikTok fetch failed: {str(e)}")

    @staticmethod
    def extract_media_info(url: str) -> MediaInfo:
        """Extract media information from TikTok URL.

        Args:
            url: TikTok URL

        Returns:
            MediaInfo object

        Raises:
            Exception: If extraction fails
        """
        try:
            media_url = TikTokProvider.extract_media_url(url)
            # Extract video ID from URL
            title = "tiktok_video"
            match = re.search(r'/video/(\d+)', url)
            if match:
                title = f"tiktok_{match.group(1)}"

            return MediaInfo(
                platform="tiktok",
                url=url,
                title=title,
                output_path="",
                status="pending",
            )

        except Exception as e:
            raise Exception(f"TikTok extraction failed: {str(e)}")
