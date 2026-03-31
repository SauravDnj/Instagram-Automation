"""
Configuration management for Instagram Automation
"""

import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Application configuration manager"""
    
    def __init__(self):
        """Initialize configuration"""
        # Load environment variables
        load_dotenv()
        
        # Base paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_dir = self.base_dir / 'data'
        self.media_dir = self.data_dir / 'media'
        self.generated_dir = self.data_dir / 'generated'
        self.resources_dir = self.base_dir / 'resources'
        
        # Database
        self.database_path = os.getenv('DATABASE_PATH', 'data/instagram_automation.db')
        
        # Instagram credentials
        self.instagram_username = os.getenv('INSTAGRAM_USERNAME', '')
        self.instagram_password = os.getenv('INSTAGRAM_PASSWORD', '')
        
        # API Keys
        self.stability_api_key = os.getenv('STABILITY_API_KEY', '')
        
        # Application settings
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # Scheduler settings
        self.timezone = os.getenv('TIMEZONE', 'UTC')
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY_SECONDS', '60'))
        
        # Security
        self.encryption_key = os.getenv('ENCRYPTION_KEY', '')
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.data_dir, self.media_dir, self.generated_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get(self, key, default=None):
        """Get configuration value by key"""
        return getattr(self, key, default)
    
    def save_credentials(self, username, password):
        """Save Instagram credentials (should be encrypted in production)"""
        # TODO: Implement encryption
        self.instagram_username = username
        self.instagram_password = password
    
    def has_instagram_credentials(self):
        """Check if Instagram credentials are configured"""
        return bool(self.instagram_username and self.instagram_password)
    
    def has_stability_key(self):
        """Check if Stability AI API key is configured"""
        return bool(self.stability_api_key)

# Global config instance
_config = None

def get_config():
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
