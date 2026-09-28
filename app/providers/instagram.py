"""Instagram provider."""
import re
import requests
from app.models import MediaInfo
from app.config import USER_AGENT, REQUEST_TIMEOUT


class InstagramProvider:
    """Handles Instagram video downloads."""

    @staticmethod
    def extract_media_url(url: str) -> str:
        """Extract direct media URL from Instagram post.

        Args:
            url: Instagram URL

        Returns:
            Direct media URL

        Raises:
            Exception: If extraction fails
        """
        try:
            # Fetch the page HTML
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            html = response.text

            # Look for video URL in og:video meta tag or JSON-LD data
            # Instagram embeds media URLs in various formats
            patterns = [
                r'"video_url":"([^"]+)"',
                r'og:video.*?content="([^"]+)"',
                r'"src":"([^"]+/videos/[^"]+)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    media_url = match.group(1)
                    # Unescape the URL
                    media_url = media_url.replace("\\/", "/")
                    return media_url

            raise Exception("Could not find video URL in Instagram post")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Instagram fetch failed: {str(e)}")

    @staticmethod
    def extract_media_info(url: str) -> MediaInfo:
        """Extract media information from Instagram URL.

        Args:
            url: Instagram URL

        Returns:
            MediaInfo object

        Raises:
            Exception: If extraction fails
        """
        try:
            media_url = InstagramProvider.extract_media_url(url)
            # Extract title from URL or use generic name
            title = "instagram_video"
            match = re.search(r'/p/([^/]+)/', url)
            if match:
                title = f"instagram_{match.group(1)[:11]}"

            return MediaInfo(
                platform="instagram",
                url=url,
                title=title,
                output_path="",
                status="pending",
            )

        except Exception as e:
            raise Exception(f"Instagram extraction failed: {str(e)}")
