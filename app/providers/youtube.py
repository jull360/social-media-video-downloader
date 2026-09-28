"""YouTube provider using yt-dlp."""
import yt_dlp
from app.models import MediaInfo
from datetime import datetime


class YouTubeProvider:
    """Handles YouTube video downloads."""

    @staticmethod
    def extract_media_info(url: str) -> MediaInfo:
        """Extract media information from YouTube URL.

        Args:
            url: YouTube URL

        Returns:
            MediaInfo object with video details

        Raises:
            Exception: If extraction fails
        """
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": "in_playlist",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            title = info.get("title", "video")
            media_url = info.get("url", url)

            return MediaInfo(
                platform="youtube",
                url=url,
                title=title,
                output_path="",
                status="pending",
            )

        except Exception as e:
            raise Exception(f"YouTube extraction failed: {str(e)}")

    @staticmethod
    def download(url: str, output_path: str) -> str:
        """Download video from YouTube.

        Args:
            url: YouTube URL
            output_path: Path to save the video

        Returns:
            Path to downloaded file

        Raises:
            Exception: If download fails
        """
        try:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "outtmpl": output_path,
                "quiet": False,
                "no_warnings": False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return filename

        except Exception as e:
            raise Exception(f"YouTube download failed: {str(e)}")
