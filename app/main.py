"""Main CLI application."""
import argparse
import sys
from datetime import datetime
from app.utils import detect_platform, get_unique_filepath
from app.downloader import Downloader
from app.config import OUTPUT_DIR
from app.providers.youtube import YouTubeProvider
from app.providers.instagram import InstagramProvider
from app.providers.tiktok import TikTokProvider


class VideoDownloaderApp:
    """Main application for downloading social media videos."""

    def __init__(self):
        """Initialize the app."""
        self.downloader = Downloader(OUTPUT_DIR)
        self.providers = {
            "youtube": YouTubeProvider,
            "instagram": InstagramProvider,
            "tiktok": TikTokProvider,
        }

    def download(self, url: str) -> bool:
        """Download a video from the given URL.

        Args:
            url: The media URL

        Returns:
            True if successful, False otherwise
        """
        print(f"\n🔍 Analyzing URL: {url}")

        # Detect platform
        platform = detect_platform(url)
        if platform == "unknown":
            print("❌ Error: Could not detect platform. Supported: YouTube, Instagram, TikTok")
            return False

        print(f"📱 Platform detected: {platform.upper()}")

        # Get the appropriate provider
        provider = self.providers.get(platform)
        if not provider:
            print(f"❌ Error: No provider for {platform}")
            return False

        try:
            # Extract media information
            print("⏳ Extracting media information...")
            if platform == "youtube":
                media_info = YouTubeProvider.extract_media_info(url)
                print(f"✓ Title: {media_info.title}")
                filepath = YouTubeProvider.download(url, OUTPUT_DIR)
                print(f"✓ Downloaded to: {filepath}")
                return True
            else:
                media_info = provider.extract_media_info(url)
                print(f"✓ Title: {media_info.title}")

                # Extract direct media URL
                media_url = provider.extract_media_url(url)
                print(f"✓ Media URL extracted")

                # Download the file
                print("⏳ Downloading...")
                filepath = self.downloader.download_url(
                    media_url,
                    media_info.title,
                    extension=".mp4"
                )
                return True

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def run(self, args=None):
        """Run the application with CLI arguments.

        Args:
            args: Command line arguments
        """
        parser = argparse.ArgumentParser(
            description="Download videos from TikTok, Instagram, and YouTube",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python -m app.main --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python -m app.main --url "https://www.instagram.com/reel/..."
  python -m app.main --url "https://www.tiktok.com/@user/video/..."
            """
        )

        parser.add_argument(
            "--url",
            "-u",
            required=True,
            help="URL of the video to download"
        )

        parsed_args = parser.parse_args(args)

        print("\n" + "="*60)
        print("  Social Media Video Downloader v0.1.0")
        print("="*60)

        success = self.download(parsed_args.url)

        if success:
            print(f"\n✓ Download completed! Files saved to: {OUTPUT_DIR}")
            return 0
        else:
            print("\n❌ Download failed!")
            return 1


if __name__ == "__main__":
    app = VideoDownloaderApp()
    sys.exit(app.run())
