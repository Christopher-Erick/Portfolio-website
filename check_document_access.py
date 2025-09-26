#!/usr/bin/env python
"""
Script to check document access in Cloudinary
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

def check_document_access():
    """Check document access in Cloudinary"""
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
        
        # Get document resources with detailed info
        result = cloudinary.api.resources(prefix="writeups/", type="upload", max_results=100, resource_type="raw")
        
        print("Document access information:")
        print("=" * 50)
        for resource in result.get('resources', []):
            public_id = resource['public_id']
            url = resource['secure_url']
            resource_type = resource.get('resource_type', 'image')
            format = resource.get('format', 'unknown')
            
            print(f"Public ID: {public_id}")
            print(f"URL: {url}")
            print(f"Resource Type: {resource_type}")
            print(f"Format: {format}")
            print("-" * 30)
        
        # Also check image resources that might be documents
        result = cloudinary.api.resources(prefix="writeups/", type="upload", max_results=100, resource_type="image")
        
        print("\nImage resources in writeups folder:")
        print("=" * 50)
        for resource in result.get('resources', []):
            public_id = resource['public_id']
            url = resource['secure_url']
            resource_type = resource.get('resource_type', 'image')
            format = resource.get('format', 'unknown')
            
            print(f"Public ID: {public_id}")
            print(f"URL: {url}")
            print(f"Resource Type: {resource_type}")
            print(f"Format: {format}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error checking document access: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_document_access()