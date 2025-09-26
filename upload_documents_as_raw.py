#!/usr/bin/env python
"""
Script to upload documents as raw files to Cloudinary
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

def upload_documents_as_raw():
    """Upload documents as raw files to Cloudinary"""
    try:
        import cloudinary
        import cloudinary.uploader
        
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
        
        # Upload writeup documents as raw files
        writeups_dir = project_dir / 'media' / 'projects' / 'writeups'
        if writeups_dir.exists():
            print("Uploading writeup documents as raw files...")
            for file_path in writeups_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.doc', '.docx']:
                    print(f"Uploading {file_path.name} as raw file...")
                    try:
                        result = cloudinary.uploader.upload(
                            str(file_path),
                            folder="writeups_raw",
                            public_id=file_path.stem,
                            resource_type="raw",
                            overwrite=True
                        )
                        print(f"  Uploaded successfully: {result['secure_url']}")
                    except Exception as e:
                        print(f"  Failed to upload {file_path.name}: {e}")
        
        print("\nRaw document upload process completed!")
        
    except Exception as e:
        print(f"Error uploading documents as raw files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    upload_documents_as_raw()