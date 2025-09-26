#!/usr/bin/env python
"""
Script to check Cloudinary configuration and test connectivity
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.conf import settings

def check_cloudinary_config():
    """Check Cloudinary configuration"""
    print("Checking Cloudinary configuration...")
    
    # Check if Cloudinary storage is configured
    default_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', '')
    print(f"DEFAULT_FILE_STORAGE: {default_storage}")
    
    if 'cloudinary' in default_storage:
        print("✓ Cloudinary storage is configured")
    else:
        print("✗ Cloudinary storage is NOT configured")
        return False
    
    # Check Cloudinary credentials
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
    api_key = getattr(settings, 'CLOUDINARY_API_KEY', None)
    api_secret = getattr(settings, 'CLOUDINARY_API_SECRET', None)
    
    if cloud_name:
        print(f"✓ CLOUDINARY_CLOUD_NAME: {cloud_name}")
    else:
        print("✗ CLOUDINARY_CLOUD_NAME is not set")
        return False
        
    if api_key:
        print("✓ CLOUDINARY_API_KEY is set")
    else:
        print("✗ CLOUDINARY_API_KEY is not set")
        return False
        
    if api_secret:
        print("✓ CLOUDINARY_API_SECRET is set")
    else:
        print("✗ CLOUDINARY_API_SECRET is not set")
        return False
    
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

if __name__ == '__main__':
    success = check_cloudinary_config()
    if success:
        print("\n✓ All Cloudinary checks passed!")
    else:
        print("\n✗ Cloudinary configuration issues detected!")
        print("Please check your environment variables and Cloudinary setup.")