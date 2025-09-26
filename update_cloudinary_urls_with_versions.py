#!/usr/bin/env python
"""
Script to update project media URLs with actual Cloudinary URLs including versions
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

from portfolio.models import Project

def update_cloudinary_urls_with_versions():
    """Update project media URLs with actual Cloudinary URLs including versions"""
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
        
        # Get all projects
        projects = Project.objects.all()
        
        # Get all resources from Cloudinary
        images = {}
        documents = {}
        
        # Get images
        result = cloudinary.api.resources(prefix="writeupsimages/", type="upload", max_results=100)
        for resource in result.get('resources', []):
            public_id = resource['public_id']
            version = resource['version']
            # Extract filename from public_id (remove folder prefix)
            filename = public_id.replace('writeupsimages/', '')
            images[filename.lower()] = f"https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}"
        
        # Get documents
        result = cloudinary.api.resources(prefix="writeups/", type="upload", max_results=100)
        for resource in result.get('resources', []):
            public_id = resource['public_id']
            version = resource['version']
            # Extract filename from public_id (remove folder prefix)
            filename = public_id.replace('writeups/', '')
            documents[filename.lower()] = f"https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}"
        
        print(f"Found {len(images)} images and {len(documents)} documents in Cloudinary")
        
        # Update project URLs
        for project in projects:
            print(f"\nProcessing project: {project.title}")
            
            # Update featured image
            if project.featured_image and project.featured_image.name:
                old_path = str(project.featured_image)
                if old_path.startswith('http'):
                    # Extract filename from old URL
                    filename = old_path.split('/')[-1].split('.')[0].lower()
                    if filename in images:
                        new_url = images[filename]
                        if old_path != new_url:
                            print(f"  Updating featured image: {old_path} -> {new_url}")
                            project.featured_image.name = new_url
                            project.save(update_fields=['featured_image'])
                        else:
                            print(f"  Featured image URL is already correct")
                    else:
                        print(f"  WARNING: Could not find image {filename} in Cloudinary")
                else:
                    print(f"  WARNING: Featured image is not a URL: {old_path}")
            
            # Update writeup document
            if project.writeup_document and project.writeup_document.name:
                old_path = str(project.writeup_document)
                if old_path.startswith('http'):
                    # Extract filename from old URL
                    filename = old_path.split('/')[-1].split('.')[0].lower()
                    if filename in documents:
                        new_url = documents[filename]
                        if old_path != new_url:
                            print(f"  Updating writeup document: {old_path} -> {new_url}")
                            project.writeup_document.name = new_url
                            project.save(update_fields=['writeup_document'])
                        else:
                            print(f"  Writeup document URL is already correct")
                    else:
                        print(f"  WARNING: Could not find document {filename} in Cloudinary")
                else:
                    print(f"  WARNING: Writeup document is not a URL: {old_path}")
        
        print("\nURL update process completed!")
        
    except Exception as e:
        print(f"Error updating Cloudinary URLs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_cloudinary_urls_with_versions()