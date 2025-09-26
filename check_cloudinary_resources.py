#!/usr/bin/env python
"""
Script to check Cloudinary resources
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
                    os.environ[key.strip()] = value.strip()

# Load environment variables
load_env_file()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

def check_cloudinary_resources():
    """Check Cloudinary resources"""
    try:
        import cloudinary
        import cloudinary.api
        
        # Get Cloudinary configuration
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        if not (cloud_name and api_key and api_secret):
            print("Missing Cloudinary credentials")
            return
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # List resources
        print("Checking Cloudinary resources...")
        result = cloudinary.api.resources(prefix="writeupsimages/", type="upload", max_results=10)
        
        print(f"Found {len(result.get('resources', []))} images in writeupsimages/ folder:")
        for resource in result.get('resources', []):
            print(f"  - {resource['public_id']}")
        
        # Check writeups folder
        result = cloudinary.api.resources(prefix="writeups/", type="upload", max_results=10)
        
        print(f"\nFound {len(result.get('resources', []))} documents in writeups/ folder:")
        for resource in result.get('resources', []):
            print(f"  - {resource['public_id']}")
            
    except Exception as e:
        print(f"Error checking Cloudinary resources: {e}")

if __name__ == '__main__':
    check_cloudinary_resources()