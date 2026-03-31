"""
Database manager for Instagram Automation
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from database.models import (
    InstagramAccount, MediaFile, Post, Schedule, 
    AIGenerationJob, AppSettings, PostType, PostStatus, ScheduleFrequency
)
from utils.logger import get_logger

logger = get_logger()

class DatabaseManager:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = "data/instagram_automation.db"):
        """Initialize database manager"""
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._initialize_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Instagram accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    session_data TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Media files table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS media_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    thumbnail_path TEXT,
                    width INTEGER,
                    height INTEGER,
                    duration REAL,
                    file_size INTEGER,
                    is_ai_generated INTEGER DEFAULT 0,
                    ai_prompt TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Posts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    media_id INTEGER NOT NULL,
                    post_type TEXT NOT NULL,
                    caption TEXT,
                    location TEXT,
                    scheduled_time TIMESTAMP,
                    posted_time TIMESTAMP,
                    status TEXT DEFAULT 'scheduled',
                    instagram_id TEXT,
                    error_message TEXT,
                    retry_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(id),
                    FOREIGN KEY (media_id) REFERENCES media_files(id)
                )
            ''')
            
            # Schedules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    time_of_day TEXT NOT NULL,
                    day_of_week INTEGER,
                    day_of_month INTEGER,
                    month INTEGER,
                    caption_template TEXT,
                    use_ai_generation INTEGER DEFAULT 0,
                    ai_prompt_template TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_run TIMESTAMP,
                    next_run TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(id)
                )
            ''')
            
            # AI generation jobs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_generation_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    negative_prompt TEXT,
                    style TEXT,
                    width INTEGER DEFAULT 512,
                    height INTEGER DEFAULT 512,
                    steps INTEGER DEFAULT 30,
                    cfg_scale REAL DEFAULT 7.0,
                    seed INTEGER,
                    media_id INTEGER,
                    status TEXT DEFAULT 'pending',
                    error_message TEXT,
                    auto_post INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (media_id) REFERENCES media_files(id)
                )
            ''')
            
            # App settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_posts_scheduled ON posts(scheduled_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_schedules_active ON schedules(is_active)')
            
            logger.info("Database initialized successfully")
    
    # Account methods
    def add_account(self, username: str, session_data: Optional[str] = None) -> int:
        """Add Instagram account"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO accounts (username, session_data) VALUES (?, ?)',
                (username, session_data)
            )
            return cursor.lastrowid
    
    def get_account(self, account_id: int) -> Optional[InstagramAccount]:
        """Get account by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
            row = cursor.fetchone()
            if row:
                return InstagramAccount(**dict(row))
            return None
    
    def get_active_accounts(self) -> List[InstagramAccount]:
        """Get all active accounts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE is_active = 1')
            return [InstagramAccount(**dict(row)) for row in cursor.fetchall()]
    
    # Media methods
    def add_media(self, media: MediaFile) -> int:
        """Add media file"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO media_files 
                (file_path, file_type, thumbnail_path, width, height, duration, 
                 file_size, is_ai_generated, ai_prompt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (media.file_path, media.file_type, media.thumbnail_path,
                  media.width, media.height, media.duration, media.file_size,
                  1 if media.is_ai_generated else 0, media.ai_prompt))
            return cursor.lastrowid
    
    def get_media(self, media_id: int) -> Optional[MediaFile]:
        """Get media by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM media_files WHERE id = ?', (media_id,))
            row = cursor.fetchone()
            if row:
                return MediaFile(**dict(row))
            return None
    
    # Post methods
    def add_post(self, post: Post) -> int:
        """Add new post"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO posts 
                (account_id, media_id, post_type, caption, location, 
                 scheduled_time, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (post.account_id, post.media_id, post.post_type.value,
                  post.caption, post.location, post.scheduled_time,
                  post.status.value))
            return cursor.lastrowid
    
    def get_scheduled_posts(self, limit: int = 100) -> List[Post]:
        """Get upcoming scheduled posts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM posts 
                WHERE status = 'scheduled' AND scheduled_time > datetime('now')
                ORDER BY scheduled_time ASC
                LIMIT ?
            ''', (limit,))
            posts = []
            for row in cursor.fetchall():
                data = dict(row)
                data['post_type'] = PostType(data['post_type'])
                data['status'] = PostStatus(data['status'])
                posts.append(Post(**data))
            return posts
    
    def update_post_status(self, post_id: int, status: PostStatus, 
                          error_message: Optional[str] = None,
                          instagram_id: Optional[str] = None):
        """Update post status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            posted_time = datetime.now() if status == PostStatus.POSTED else None
            cursor.execute('''
                UPDATE posts 
                SET status = ?, error_message = ?, instagram_id = ?, 
                    posted_time = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status.value, error_message, instagram_id, posted_time, post_id))
    
    # Schedule methods
    def add_schedule(self, schedule: Schedule) -> int:
        """Add new schedule"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO schedules 
                (account_id, name, post_type, frequency, time_of_day,
                 day_of_week, day_of_month, month, caption_template,
                 use_ai_generation, ai_prompt_template, next_run)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (schedule.account_id, schedule.name, schedule.post_type.value,
                  schedule.frequency.value, schedule.time_of_day,
                  schedule.day_of_week, schedule.day_of_month, schedule.month,
                  schedule.caption_template, 1 if schedule.use_ai_generation else 0,
                  schedule.ai_prompt_template, schedule.next_run))
            return cursor.lastrowid
    
    def get_active_schedules(self) -> List[Schedule]:
        """Get all active schedules"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM schedules WHERE is_active = 1')
            schedules = []
            for row in cursor.fetchall():
                data = dict(row)
                data['post_type'] = PostType(data['post_type'])
                data['frequency'] = ScheduleFrequency(data['frequency'])
                schedules.append(Schedule(**data))
            return schedules
    
    # Settings methods
    def get_setting(self, key: str) -> Optional[str]:
        """Get setting value by key"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM app_settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
    
    def set_setting(self, key: str, value: str):
        """Set setting value"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO app_settings (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP
            ''', (key, value, value))
