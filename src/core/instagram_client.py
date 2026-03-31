"""
Instagram Client - 100% FREE
Only requires Instagram username and password - NO API KEYS!
"""

import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, 
    ChallengeRequired,
    TwoFactorRequired,
    PleaseWaitFewMinutes
)

from utils.logger import get_logger
from utils.config import get_config

logger = get_logger()

class InstagramClient:
    """
    Free Instagram client using instagrapi
    No API keys required - just username and password!
    """
    
    def __init__(self):
        """Initialize Instagram client"""
        self.client = Client()
        self.config = get_config()
        self.session_file = "data/instagram_session.json"
        self.is_logged_in = False
        self.username = None
        
    def login(self, username: str, password: str, verification_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Login to Instagram - 100% FREE!
        
        Args:
            username: Instagram username
            password: Instagram password
            verification_code: Optional 2FA code if enabled
            
        Returns:
            Dict with success status and message
        """
        try:
            logger.info(f"Attempting login for user: {username}")
            
            # Try to load existing session first
            if os.path.exists(self.session_file):
                try:
                    logger.info("Found existing session, attempting to reuse...")
                    self.client.load_settings(self.session_file)
                    self.client.login(username, password)
                    
                    # Verify session is valid
                    self.client.get_timeline_feed()
                    
                    self.is_logged_in = True
                    self.username = username
                    logger.info("Successfully logged in using existing session!")
                    return {
                        'success': True,
                        'message': 'Logged in successfully (existing session)',
                        'username': username
                    }
                except Exception as e:
                    logger.warning(f"Existing session invalid: {e}")
                    # Continue to fresh login
            
            # Fresh login
            logger.info("Performing fresh login...")
            
            # Handle 2FA if code provided
            if verification_code:
                self.client.two_factor_login(username, password, verification_code)
            else:
                self.client.login(username, password)
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            
            self.is_logged_in = True
            self.username = username
            
            logger.info(f"Successfully logged in as {username}!")
            return {
                'success': True,
                'message': 'Logged in successfully!',
                'username': username
            }
            
        except TwoFactorRequired as e:
            logger.warning("Two-factor authentication required")
            return {
                'success': False,
                'message': 'Two-factor authentication code required',
                'requires_2fa': True
            }
            
        except ChallengeRequired as e:
            logger.warning("Instagram challenge required")
            return {
                'success': False,
                'message': 'Instagram security challenge required. Please verify your account on Instagram app.',
                'requires_challenge': True
            }
            
        except PleaseWaitFewMinutes as e:
            logger.warning("Rate limited by Instagram")
            return {
                'success': False,
                'message': 'Too many login attempts. Please wait a few minutes and try again.'
            }
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return {
                'success': False,
                'message': f'Login failed: {str(e)}'
            }
    
    def logout(self):
        """Logout and clear session"""
        try:
            if self.is_logged_in:
                self.client.logout()
                self.is_logged_in = False
                self.username = None
                
                # Remove session file
                if os.path.exists(self.session_file):
                    os.remove(self.session_file)
                
                logger.info("Logged out successfully")
                return {'success': True, 'message': 'Logged out successfully'}
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return {'success': False, 'message': f'Logout error: {str(e)}'}
    
    def post_photo(self, image_path: str, caption: str = "") -> Dict[str, Any]:
        """
        Post a photo to Instagram - FREE!
        
        Args:
            image_path: Path to image file
            caption: Photo caption (optional)
            
        Returns:
            Dict with success status and post info
        """
        if not self.is_logged_in:
            return {'success': False, 'message': 'Not logged in'}
        
        try:
            logger.info(f"Posting photo: {image_path}")
            
            # Upload photo
            media = self.client.photo_upload(
                path=image_path,
                caption=caption
            )
            
            logger.info(f"Photo posted successfully! Media ID: {media.pk}")
            return {
                'success': True,
                'message': 'Photo posted successfully!',
                'media_id': media.pk,
                'code': media.code
            }
            
        except Exception as e:
            logger.error(f"Failed to post photo: {e}")
            return {
                'success': False,
                'message': f'Failed to post photo: {str(e)}'
            }
    
    def post_video(self, video_path: str, caption: str = "", thumbnail_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a video/reel to Instagram - FREE!
        
        Args:
            video_path: Path to video file
            caption: Video caption (optional)
            thumbnail_path: Path to custom thumbnail (optional)
            
        Returns:
            Dict with success status and post info
        """
        if not self.is_logged_in:
            return {'success': False, 'message': 'Not logged in'}
        
        try:
            logger.info(f"Posting video: {video_path}")
            
            # Upload video as reel
            media = self.client.clip_upload(
                path=video_path,
                caption=caption,
                thumbnail=thumbnail_path
            )
            
            logger.info(f"Video/Reel posted successfully! Media ID: {media.pk}")
            return {
                'success': True,
                'message': 'Video/Reel posted successfully!',
                'media_id': media.pk,
                'code': media.code
            }
            
        except Exception as e:
            logger.error(f"Failed to post video: {e}")
            return {
                'success': False,
                'message': f'Failed to post video: {str(e)}'
            }
    
    def post_story_photo(self, image_path: str) -> Dict[str, Any]:
        """
        Post a photo story to Instagram - FREE!
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with success status and story info
        """
        if not self.is_logged_in:
            return {'success': False, 'message': 'Not logged in'}
        
        try:
            logger.info(f"Posting story photo: {image_path}")
            
            # Upload story photo
            story = self.client.photo_upload_to_story(
                path=image_path
            )
            
            logger.info(f"Story posted successfully! Story ID: {story.pk}")
            return {
                'success': True,
                'message': 'Story posted successfully!',
                'story_id': story.pk
            }
            
        except Exception as e:
            logger.error(f"Failed to post story: {e}")
            return {
                'success': False,
                'message': f'Failed to post story: {str(e)}'
            }
    
    def post_story_video(self, video_path: str) -> Dict[str, Any]:
        """
        Post a video story to Instagram - FREE!
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dict with success status and story info
        """
        if not self.is_logged_in:
            return {'success': False, 'message': 'Not logged in'}
        
        try:
            logger.info(f"Posting story video: {video_path}")
            
            # Upload story video
            story = self.client.video_upload_to_story(
                path=video_path
            )
            
            logger.info(f"Story video posted successfully! Story ID: {story.pk}")
            return {
                'success': True,
                'message': 'Story video posted successfully!',
                'story_id': story.pk
            }
            
        except Exception as e:
            logger.error(f"Failed to post story video: {e}")
            return {
                'success': False,
                'message': f'Failed to post story video: {str(e)}'
            }
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get current account information - FREE!
        
        Returns:
            Dict with account information
        """
        if not self.is_logged_in:
            return {'success': False, 'message': 'Not logged in'}
        
        try:
            user_info = self.client.account_info()
            
            return {
                'success': True,
                'username': user_info.username,
                'full_name': user_info.full_name,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count
            }
            
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return {
                'success': False,
                'message': f'Failed to get account info: {str(e)}'
            }

# Global client instance
_client = None

def get_instagram_client() -> InstagramClient:
    """Get global Instagram client instance"""
    global _client
    if _client is None:
        _client = InstagramClient()
    return _client
