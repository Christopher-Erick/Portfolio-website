import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

# Setup Django
django.setup()

# Import the config
from config import PersonalConfig, SocialConfig

print("Testing Social Links Configuration:")
print("=" * 40)

# Test personal info
print(f"Full Name: {PersonalConfig.get_full_name()}")
print(f"Email: {PersonalConfig.get_email()}")
print(f"GitHub Username: {PersonalConfig.get_github_username()}")
print(f"TryHackMe Username: {PersonalConfig.get_tryhackme_username()}")
print(f"HackTheBox Username: {PersonalConfig.get_hackthebox_username()}")
print()

# Test social URLs
print(f"GitHub URL: {SocialConfig.get_github_url()}")
print(f"TryHackMe URL: {SocialConfig.get_tryhackme_url()}")
print(f"HackTheBox URL: {SocialConfig.get_hackthebox_url()}")
print(f"Email URL: {SocialConfig.get_email_url()}")