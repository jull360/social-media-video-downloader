"""Configuration module."""
import os
from dotenv import load_dotenv

load_dotenv()

# Directories
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Request settings
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Platforms
PLATFORMS = {
    "youtube": ["youtube.com", "youtu.be", "m.youtube.com"],
    "instagram": ["instagram.com", "www.instagram.com"],
    "tiktok": ["tiktok.com", "www.tiktok.com", "vm.tiktok.com", "vt.tiktok.com"],
}
