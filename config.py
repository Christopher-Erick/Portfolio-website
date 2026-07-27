"""
Secure configuration loader for portfolio project
Loads configuration values strictly from environment variables
"""

import os
from pathlib import Path

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

load_env_file()

class PersonalConfig:
    """Personal information configuration"""
    
    @staticmethod
    def get_full_name():
        return os.getenv('FULL_NAME', 'Christopher Erick Otieno')
    
    @staticmethod
    def get_email():
        return os.getenv('EMAIL', 'christophererick879@gmail.com')
    
    @staticmethod
    def get_github_username():
        return os.getenv('GITHUB_USERNAME', 'Christopher-Erick')
    
    @staticmethod
    def get_tryhackme_username():
        return os.getenv('TRYHACKME_USERNAME', 'erikchris54')
    
    @staticmethod
    def get_hackthebox_username():
        return os.getenv('HACKTHEBOX_USERNAME', 'ChristopherErick')
    
    @staticmethod
    def get_tagline():
        return os.getenv('TAGLINE', 'Cybersecurity Professional & Software Engineer')
    
    @staticmethod
    def get_phone():
        return os.getenv('PHONE', '+254758081580')
    
    @staticmethod
    def get_location():
        return os.getenv('LOCATION', 'Nairobi, Kenya')

class AdminConfig:
    """Admin configuration"""
    
    @staticmethod
    def get_admin_username():
        return os.getenv('ADMIN_USERNAME', 'admin')
    
    @staticmethod
    def get_admin_email():
        return os.getenv('ADMIN_EMAIL', PersonalConfig.get_email())

class SocialConfig:
    """Social media and professional platform URLs"""
    
    @staticmethod
    def get_github_url():
        username = PersonalConfig.get_github_username()
        return f'https://github.com/{username}' if username else '#'
    
    @staticmethod
    def get_tryhackme_url():
        username = PersonalConfig.get_tryhackme_username()
        return f'https://tryhackme.com/p/{username}' if username else '#'
    
    @staticmethod
    def get_hackthebox_url():
        username = PersonalConfig.get_hackthebox_username()
        return f'https://app.hackthebox.com/users/{username}' if username else '#'
    
    @staticmethod
    def get_email_url():
        email = PersonalConfig.get_email()
        return f'mailto:{email}' if email else '#'
