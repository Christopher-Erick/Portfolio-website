#!/usr/bin/env python
"""
Script to load environment variables and test Cloudinary integration
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

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

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.conf import settings

def test_cloudinary():
    """Test Cloudinary configuration"""
    print("Testing Cloudinary configuration...")
    
    # Check if Cloudinary storage is configured
    default_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', '')
    print(f"DEFAULT_FILE_STORAGE: {default_storage}")
    
    # Check Cloudinary credentials
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
    api_key = getattr(settings, 'CLOUDINARY_API_KEY', None)
    api_secret = getattr(settings, 'CLOUDINARY_API_SECRET', None)
    
    print(f"CLOUDINARY_CLOUD_NAME: {cloud_name}")
    print(f"CLOUDINARY_API_KEY: {'SET' if api_key else 'NOT SET'}")
    print(f"CLOUDINARY_API_SECRET: {'SET' if api_secret else 'NOT SET'}")
    
    if cloud_name and api_key and api_secret:
        print("\n✓ All Cloudinary credentials are set")
        
        # Try to import Cloudinary
        try:
            import cloudinary
            print("✓ Cloudinary package is available")
            
            # Configure Cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            # Test connectivity
            import cloudinary.api
            result = cloudinary.api.ping()
            if result.get('error'):
                print(f"✗ Cloudinary API error: {result['error']}")
                return False
            else:
                print("✓ Cloudinary API connectivity test passed")
                return True
                
        except ImportError:
            print("✗ Cloudinary package is not installed")
            return False
        except Exception as e:
            print(f"✗ Cloudinary connectivity test failed: {e}")
            return False
    else:
        print("\n✗ Missing Cloudinary credentials")
        return False

if __name__ == '__main__':
    success = test_cloudinary()
    if success:
        print("\n✓ Cloudinary is properly configured!")
    else:
        print("\n✗ Cloudinary configuration issues detected!")