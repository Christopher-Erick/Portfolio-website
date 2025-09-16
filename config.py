"""
Secure configuration loader for portfolio project
Loads sensitive data from environment variables or .env file
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

# Load .env file on import
load_env_file()

# Personal Information Configuration
class PersonalConfig:
    """Secure personal information configuration"""
    
    @staticmethod
    def get_full_name():
        return os.getenv('FULL_NAME', 'Your Name')
    
    @staticmethod
    def get_email():
        return os.getenv('EMAIL', 'your.email@domain.com')
    
    @staticmethod
    def get_github_username():
        return os.getenv('GITHUB_USERNAME', 'your-username')
    
    @staticmethod
    def get_tryhackme_username():
        return os.getenv('TRYHACKME_USERNAME', 'your-username')
    
    @staticmethod
    def get_hackthebox_username():
        return os.getenv('HACKTHEBOX_USERNAME', 'your-username')
    
    @staticmethod
    def get_tagline():
        return os.getenv('TAGLINE', 'Your professional tagline')
    
    @staticmethod
    def get_phone():
        return os.getenv('PHONE', '')
    
    @staticmethod
    def get_location():
        return os.getenv('LOCATION', '')

# Admin Configuration
class AdminConfig:
    """Secure admin configuration"""
    
    @staticmethod
    def get_admin_username():
        return os.getenv('ADMIN_USERNAME', 'admin')
    
    @staticmethod
    def get_admin_email():
        return os.getenv('ADMIN_EMAIL', PersonalConfig.get_email())

# Social Media URLs
class SocialConfig:
    """Social media and professional platform URLs"""
    
    @staticmethod
    def get_github_url():
        username = PersonalConfig.get_github_username()
        return f'https://github.com/{username}' if username != 'your-username' else '#'
    
    @staticmethod
    def get_tryhackme_url():
        username = PersonalConfig.get_tryhackme_username()
        return f'https://tryhackme.com/p/{username}' if username != 'your-username' else '#'
    
    @staticmethod
    def get_hackthebox_url():
        username = PersonalConfig.get_hackthebox_username()
        return f'https://app.hackthebox.com/profile/{username}' if username != 'your-username' else '#'
    
    @staticmethod
    def get_email_url():
        email = PersonalConfig.get_email()
        return f'mailto:{email}' if email != 'your.email@domain.com' else '#'