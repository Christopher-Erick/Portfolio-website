import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

# Clear any existing Django setup
if 'django' in sys.modules:
    del sys.modules['django']
if 'portfolio_site' in sys.modules:
    del sys.modules['portfolio_site']
if 'portfolio_site.settings' in sys.modules:
    del sys.modules['portfolio_site.settings']

# Clear environment variables that might be cached
for key in list(os.environ.keys()):
    if key.startswith('DJANGO_'):
        del os.environ[key]

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = project_dir / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()  # Override, not setdefault

# Load environment variables
load_env_file()

print("Environment variables:")
print("DEBUG:", os.environ.get('DEBUG', 'Not set'))
print("CLOUDINARY_CLOUD_NAME:", os.environ.get('CLOUDINARY_CLOUD_NAME', 'Not set'))
print("CLOUDINARY_API_KEY:", os.environ.get('CLOUDINARY_API_KEY', 'Not set'))
print("CLOUDINARY_API_SECRET:", os.environ.get('CLOUDINARY_API_SECRET', 'Not set'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

import django
django.setup()

from django.conf import settings

# Print Django settings
print("\nDjango settings:")
print("DEBUG:", getattr(settings, 'DEBUG', 'Not set'))
print("CLOUDINARY_CLOUD_NAME:", getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'Not set'))
print("CLOUDINARY_API_KEY:", getattr(settings, 'CLOUDINARY_API_KEY', 'Not set'))
print("CLOUDINARY_API_SECRET:", getattr(settings, 'CLOUDINARY_API_SECRET', 'Not set'))
print("DEFAULT_FILE_STORAGE:", getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set'))