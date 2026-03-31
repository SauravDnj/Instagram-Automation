"""
Data models for Instagram Automation
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class PostType(Enum):
    """Post type enumeration"""
    IMAGE = "image"
    REEL = "reel"
    STORY = "story"

class ScheduleFrequency(Enum):
    """Schedule frequency types"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class PostStatus(Enum):
    """Post status enumeration"""
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class InstagramAccount:
    """Instagram account model"""
    id: Optional[int] = None
    username: str = ""
    session_data: Optional[str] = None  # Encrypted session
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class MediaFile:
    """Media file model"""
    id: Optional[int] = None
    file_path: str = ""
    file_type: str = ""  # image, video
    thumbnail_path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None  # For videos
    file_size: Optional[int] = None
    is_ai_generated: bool = False
    ai_prompt: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Post:
    """Post model"""
    id: Optional[int] = None
    account_id: int = 0
    media_id: int = 0
    post_type: PostType = PostType.IMAGE
    caption: str = ""
    location: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    posted_time: Optional[datetime] = None
    status: PostStatus = PostStatus.SCHEDULED
    instagram_id: Optional[str] = None  # Instagram post ID after posting
    error_message: Optional[str] = None
    retry_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Schedule:
    """Recurring schedule model"""
    id: Optional[int] = None
    account_id: int = 0
    name: str = ""
    post_type: PostType = PostType.IMAGE
    frequency: ScheduleFrequency = ScheduleFrequency.DAILY
    time_of_day: str = "12:00"  # HH:MM format
    day_of_week: Optional[int] = None  # 0-6 for weekly
    day_of_month: Optional[int] = None  # 1-31 for monthly
    month: Optional[int] = None  # 1-12 for yearly
    caption_template: str = ""
    use_ai_generation: bool = False
    ai_prompt_template: Optional[str] = None
    is_active: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class AIGenerationJob:
    """AI image generation job model"""
    id: Optional[int] = None
    prompt: str = ""
    negative_prompt: Optional[str] = None
    style: Optional[str] = None
    width: int = 512
    height: int = 512
    steps: int = 30
    cfg_scale: float = 7.0
    seed: Optional[int] = None
    media_id: Optional[int] = None  # Link to generated media
    status: str = "pending"  # pending, generating, completed, failed
    error_message: Optional[str] = None
    auto_post: bool = False
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class AppSettings:
    """Application settings model"""
    id: Optional[int] = None
    key: str = ""
    value: str = ""
    updated_at: Optional[datetime] = None
