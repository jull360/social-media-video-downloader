"""Data models for media information."""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MediaInfo:
    """Represents downloaded media information."""
    platform: str
    url: str
    title: str
    output_path: str
    status: str  # 'success', 'failed', 'pending'
    downloaded_at: Optional[datetime] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None

    def __str__(self) -> str:
        return f"[{self.platform.upper()}] {self.title} - {self.status}"
