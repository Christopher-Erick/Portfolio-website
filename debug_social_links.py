import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

# Setup Django
django.setup()

# Now test the config
from config import PersonalConfig, SocialConfig

print("Environment Variables:")
print(f"GITHUB_USERNAME: {os.getenv('GITHUB_USERNAME')}")
print(f"TRYHACKME_USERNAME: {os.getenv('TRYHACKME_USERNAME')}")
print(f"HACKTHEBOX_USERNAME: {os.getenv('HACKTHEBOX_USERNAME')}")

print("\nGenerated URLs:")
print(f"GitHub URL: {SocialConfig.get_github_url()}")
print(f"TryHackMe URL: {SocialConfig.get_tryhackme_url()}")
print(f"HackTheBox URL: {SocialConfig.get_hackthebox_url()}")

print("\nPersonal Config:")
print(f"GitHub Username: {PersonalConfig.get_github_username()}")
print(f"TryHackMe Username: {PersonalConfig.get_tryhackme_username()}")
print(f"HackTheBox Username: {PersonalConfig.get_hackthebox_username()}")