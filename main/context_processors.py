"""
Context processors to make secure configuration available to templates
"""
from config import PersonalConfig, SocialConfig
import os


def personal_info(request):
    """Add personal information to template context"""
    return {
        'PERSONAL_NAME': PersonalConfig.get_full_name(),
        'PERSONAL_EMAIL': PersonalConfig.get_email(),
        'PERSONAL_TAGLINE': PersonalConfig.get_tagline(),
        'PERSONAL_PHONE': PersonalConfig.get_phone(),
        'PERSONAL_LOCATION': PersonalConfig.get_location(),
        'GITHUB_URL': SocialConfig.get_github_url(),
        'TRYHACKME_URL': SocialConfig.get_tryhackme_url(),
        'HACKTHEBOX_URL': SocialConfig.get_hackthebox_url(),
        'EMAIL_URL': SocialConfig.get_email_url(),
        'GITHUB_USERNAME': PersonalConfig.get_github_username(),
        'ADMIN_URL': os.getenv('ADMIN_URL', 'admin/'),
    }