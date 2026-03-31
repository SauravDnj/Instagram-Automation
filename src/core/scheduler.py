"""
Scheduler System - 100% FREE
Schedule Instagram posts for daily, weekly, monthly, yearly, or custom dates
"""

import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from core.instagram_client import get_instagram_client
from database.db_manager import DatabaseManager
from database.models import Post, Schedule, PostType, PostStatus, ScheduleFrequency
from utils.logger import get_logger
from utils.config import get_config

logger = get_logger()

class PostScheduler:
    """
    Instagram post scheduler - 100% FREE!
    Schedule posts for future dates with no API keys required
    """
    
    def __init__(self):
        """Initialize scheduler"""
        self.config = get_config()
        self.db = DatabaseManager(self.config.database_path)
        self.instagram_client = get_instagram_client()
        
        # Configure job store
        jobstores = {
            'default': SQLAlchemyJobStore(url=f'sqlite:///{self.config.database_path}')
        }
        
        executors = {
            'default': ThreadPoolExecutor(10)
        }
        
        job_defaults = {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': 300  # 5 minutes
        }
        
        # Create scheduler
        self.scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=self.config.timezone
        )
        
        self.is_running = False
        logger.info("Post scheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")
            
            # Reload any existing schedules
            self._reload_schedules()
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
    
    def schedule_post(
        self,
        media_path: str,
        post_type: PostType,
        caption: str,
        scheduled_time: datetime,
        account_id: int = 1
    ) -> Dict[str, Any]:
        """
        Schedule a one-time post
        
        Args:
            media_path: Path to media file
            post_type: Type of post (photo, video, story)
            caption: Post caption
            scheduled_time: When to post
            account_id: Instagram account ID
            
        Returns:
            Dict with success status and post info
        """
        try:
            # Validate scheduled time is in future
            if scheduled_time <= datetime.now():
                return {
                    'success': False,
                    'message': 'Scheduled time must be in the future'
                }
            
            # Add media to database
            from database.models import MediaFile
            from PIL import Image
            
            media = MediaFile()
            media.file_path = media_path
            
            # Determine file type
            if media_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                media.file_type = 'video'
            else:
                media.file_type = 'image'
                # Get image dimensions
                try:
                    img = Image.open(media_path)
                    media.width, media.height = img.size
                except:
                    pass
            
            media.file_size = os.path.getsize(media_path)
            media_id = self.db.add_media(media)
            
            # Create post in database
            post = Post()
            post.account_id = account_id
            post.media_id = media_id
            post.post_type = post_type
            post.caption = caption
            post.scheduled_time = scheduled_time
            post.status = PostStatus.SCHEDULED
            
            post_id = self.db.add_post(post)
            
            # Schedule the job
            job = self.scheduler.add_job(
                func=self._execute_post,
                trigger=DateTrigger(run_date=scheduled_time),
                args=[post_id],
                id=f'post_{post_id}',
                replace_existing=True
            )
            
            logger.info(f"Scheduled post {post_id} for {scheduled_time}")
            
            return {
                'success': True,
                'message': f'Post scheduled for {scheduled_time.strftime("%Y-%m-%d %H:%M")}',
                'post_id': post_id,
                'scheduled_time': scheduled_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to schedule post: {e}")
            return {
                'success': False,
                'message': f'Failed to schedule post: {str(e)}'
            }
    
    def create_recurring_schedule(
        self,
        name: str,
        post_type: PostType,
        frequency: ScheduleFrequency,
        time_of_day: str,  # HH:MM format
        caption_template: str,
        media_folder: str,  # Folder to pick media from
        account_id: int = 1,
        day_of_week: Optional[int] = None,  # 0-6 for weekly
        day_of_month: Optional[int] = None,  # 1-31 for monthly
        month: Optional[int] = None  # 1-12 for yearly
    ) -> Dict[str, Any]:
        """
        Create a recurring schedule
        
        Args:
            name: Schedule name
            post_type: Type of post
            frequency: How often (daily, weekly, monthly, yearly)
            time_of_day: Time to post (HH:MM)
            caption_template: Caption template
            media_folder: Folder containing media files
            account_id: Instagram account ID
            day_of_week: Day for weekly (0=Monday, 6=Sunday)
            day_of_month: Day for monthly (1-31)
            month: Month for yearly (1-12)
            
        Returns:
            Dict with success status and schedule info
        """
        try:
            # Parse time
            hour, minute = map(int, time_of_day.split(':'))
            
            # Create cron trigger based on frequency
            if frequency == ScheduleFrequency.DAILY:
                trigger = CronTrigger(hour=hour, minute=minute)
            elif frequency == ScheduleFrequency.WEEKLY:
                if day_of_week is None:
                    return {'success': False, 'message': 'Day of week required for weekly schedule'}
                trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute)
            elif frequency == ScheduleFrequency.MONTHLY:
                if day_of_month is None:
                    return {'success': False, 'message': 'Day of month required for monthly schedule'}
                trigger = CronTrigger(day=day_of_month, hour=hour, minute=minute)
            elif frequency == ScheduleFrequency.YEARLY:
                if month is None or day_of_month is None:
                    return {'success': False, 'message': 'Month and day required for yearly schedule'}
                trigger = CronTrigger(month=month, day=day_of_month, hour=hour, minute=minute)
            else:
                return {'success': False, 'message': 'Invalid frequency'}
            
            # Save schedule to database
            schedule = Schedule()
            schedule.account_id = account_id
            schedule.name = name
            schedule.post_type = post_type
            schedule.frequency = frequency
            schedule.time_of_day = time_of_day
            schedule.day_of_week = day_of_week
            schedule.day_of_month = day_of_month
            schedule.month = month
            schedule.caption_template = caption_template
            schedule.is_active = True
            
            schedule_id = self.db.add_schedule(schedule)
            
            # Add recurring job
            job = self.scheduler.add_job(
                func=self._execute_recurring_post,
                trigger=trigger,
                args=[schedule_id, media_folder],
                id=f'schedule_{schedule_id}',
                replace_existing=True
            )
            
            logger.info(f"Created recurring schedule {schedule_id}: {name}")
            
            return {
                'success': True,
                'message': f'Recurring schedule created: {name}',
                'schedule_id': schedule_id
            }
            
        except Exception as e:
            logger.error(f"Failed to create recurring schedule: {e}")
            return {
                'success': False,
                'message': f'Failed to create schedule: {str(e)}'
            }
    
    def cancel_post(self, post_id: int) -> Dict[str, Any]:
        """Cancel a scheduled post"""
        try:
            job_id = f'post_{post_id}'
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            
            self.db.update_post_status(post_id, PostStatus.CANCELLED)
            
            logger.info(f"Cancelled post {post_id}")
            return {
                'success': True,
                'message': 'Post cancelled successfully'
            }
        except Exception as e:
            logger.error(f"Failed to cancel post: {e}")
            return {
                'success': False,
                'message': f'Failed to cancel post: {str(e)}'
            }
    
    def get_scheduled_posts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get list of upcoming scheduled posts"""
        posts = self.db.get_scheduled_posts(limit)
        
        result = []
        for post in posts:
            media = self.db.get_media(post.media_id)
            result.append({
                'id': post.id,
                'type': post.post_type.value,
                'caption': post.caption[:50] + '...' if len(post.caption) > 50 else post.caption,
                'scheduled_time': post.scheduled_time.strftime('%Y-%m-%d %H:%M'),
                'media_path': media.file_path if media else None,
                'status': post.status.value
            })
        
        return result
    
    def _execute_post(self, post_id: int):
        """Execute a scheduled post (internal)"""
        logger.info(f"Executing scheduled post {post_id}")
        
        try:
            # Get post from database
            from database.models import Post
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
                row = cursor.fetchone()
                
                if not row:
                    logger.error(f"Post {post_id} not found")
                    return
                
                post_data = dict(row)
                post_data['post_type'] = PostType(post_data['post_type'])
                post_data['status'] = PostStatus(post_data['status'])
                post = Post(**post_data)
            
            # Get media
            media = self.db.get_media(post.media_id)
            if not media:
                logger.error(f"Media not found for post {post_id}")
                self.db.update_post_status(post_id, PostStatus.FAILED, "Media file not found")
                return
            
            # Check if file still exists
            if not os.path.exists(media.file_path):
                logger.error(f"Media file not found: {media.file_path}")
                self.db.update_post_status(post_id, PostStatus.FAILED, "Media file not found on disk")
                return
            
            # Post to Instagram
            result = None
            
            if post.post_type == PostType.IMAGE:
                result = self.instagram_client.post_photo(media.file_path, post.caption)
            elif post.post_type == PostType.REEL:
                result = self.instagram_client.post_video(media.file_path, post.caption)
            elif post.post_type == PostType.STORY:
                if media.file_type == 'video':
                    result = self.instagram_client.post_story_video(media.file_path)
                else:
                    result = self.instagram_client.post_story_photo(media.file_path)
            
            # Update post status
            if result and result.get('success'):
                self.db.update_post_status(
                    post_id,
                    PostStatus.POSTED,
                    instagram_id=result.get('media_id') or result.get('story_id')
                )
                logger.info(f"Post {post_id} executed successfully")
            else:
                error_msg = result.get('message') if result else 'Unknown error'
                self.db.update_post_status(post_id, PostStatus.FAILED, error_msg)
                logger.error(f"Post {post_id} failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error executing post {post_id}: {e}")
            self.db.update_post_status(post_id, PostStatus.FAILED, str(e))
    
    def _execute_recurring_post(self, schedule_id: int, media_folder: str):
        """Execute a recurring schedule (internal)"""
        logger.info(f"Executing recurring schedule {schedule_id}")
        
        try:
            # Get schedule from database
            schedules = self.db.get_active_schedules()
            schedule = next((s for s in schedules if s.id == schedule_id), None)
            
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return
            
            # Pick a random media file from folder
            if not os.path.exists(media_folder):
                logger.error(f"Media folder not found: {media_folder}")
                return
            
            media_files = [f for f in os.listdir(media_folder) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
            
            if not media_files:
                logger.error(f"No media files found in {media_folder}")
                return
            
            import random
            media_file = os.path.join(media_folder, random.choice(media_files))
            
            # Create and execute post
            result = self.schedule_post(
                media_path=media_file,
                post_type=schedule.post_type,
                caption=schedule.caption_template,
                scheduled_time=datetime.now() + timedelta(seconds=5),  # Post in 5 seconds
                account_id=schedule.account_id
            )
            
            if result.get('success'):
                logger.info(f"Recurring post created from schedule {schedule_id}")
            else:
                logger.error(f"Failed to create recurring post: {result.get('message')}")
                
        except Exception as e:
            logger.error(f"Error executing recurring schedule {schedule_id}: {e}")
    
    def _reload_schedules(self):
        """Reload existing schedules from database"""
        try:
            # Reload scheduled posts
            posts = self.db.get_scheduled_posts(1000)
            for post in posts:
                if post.scheduled_time > datetime.now():
                    self.scheduler.add_job(
                        func=self._execute_post,
                        trigger=DateTrigger(run_date=post.scheduled_time),
                        args=[post.id],
                        id=f'post_{post.id}',
                        replace_existing=True
                    )
            
            logger.info(f"Reloaded {len(posts)} scheduled posts")
            
        except Exception as e:
            logger.error(f"Error reloading schedules: {e}")

# Global scheduler instance
_scheduler = None

def get_scheduler() -> PostScheduler:
    """Get global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = PostScheduler()
    return _scheduler
