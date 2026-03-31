"""
Input validation utilities
"""

import re
from datetime import datetime
from typing import Optional, Tuple

class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_instagram_username(username: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Instagram username format
        
        Args:
            username: Instagram username to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) > 30:
            return False, "Username must be 30 characters or less"
        
        # Instagram usernames can only contain letters, numbers, periods, and underscores
        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            return False, "Username can only contain letters, numbers, periods, and underscores"
        
        return True, None
    
    @staticmethod
    def validate_caption(caption: str, max_length: int = 2200) -> Tuple[bool, Optional[str]]:
        """
        Validate Instagram caption
        
        Args:
            caption: Caption text
            max_length: Maximum allowed length
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(caption) > max_length:
            return False, f"Caption must be {max_length} characters or less"
        
        return True, None
    
    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file path exists and is readable
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        import os
        
        if not file_path:
            return False, "File path cannot be empty"
        
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        if not os.path.isfile(file_path):
            return False, "Path is not a file"
        
        return True, None
    
    @staticmethod
    def validate_image_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate image file type and readability
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid, error = Validators.validate_file_path(file_path)
        if not valid:
            return valid, error
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in allowed_extensions:
            return False, f"Invalid image format. Allowed: {', '.join(allowed_extensions)}"
        
        return True, None
    
    @staticmethod
    def validate_video_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate video file type
        
        Args:
            file_path: Path to video file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid, error = Validators.validate_file_path(file_path)
        if not valid:
            return valid, error
        
        # Check file extension
        allowed_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in allowed_extensions:
            return False, f"Invalid video format. Allowed: {', '.join(allowed_extensions)}"
        
        return True, None
    
    @staticmethod
    def validate_schedule_date(date_time: datetime) -> Tuple[bool, Optional[str]]:
        """
        Validate scheduled date is in the future
        
        Args:
            date_time: Scheduled datetime
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if date_time <= datetime.now():
            return False, "Scheduled time must be in the future"
        
        return True, None
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
        """
        Validate API key format
        
        Args:
            api_key: API key string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not api_key:
            return False, "API key cannot be empty"
        
        if len(api_key) < 10:
            return False, "API key appears to be invalid (too short)"
        
        return True, None
