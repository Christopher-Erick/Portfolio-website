#!/usr/bin/env python
"""
Script to verify that all project media URLs are accessible
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from portfolio.models import Project

def verify_project_media():
    """Verify that all project media URLs are accessible"""
    import requests
    from requests.exceptions import RequestException
    
    # Get all projects
    projects = Project.objects.all()
    
    print("Verifying project media URLs...")
    print("=" * 50)
    
    all_good = True
    
    for project in projects:
        print(f"\nProject: {project.title}")
        
        # Check featured image
        if project.featured_image and project.featured_image.name:
            url = str(project.featured_image)
            if url.startswith('http'):
                try:
                    response = requests.head(url, timeout=10)
                    if response.status_code == 200:
                        print(f"  ✓ Featured image: OK")
                    else:
                        print(f"  ✗ Featured image: HTTP {response.status_code}")
                        all_good = False
                except RequestException as e:
                    print(f"  ✗ Featured image: {e}")
                    all_good = False
            else:
                print(f"  ? Featured image: Local file ({url})")
        else:
            print(f"  - Featured image: None")
        
        # Check writeup document
        if project.writeup_document and project.writeup_document.name:
            url = str(project.writeup_document)
            if url.startswith('http'):
                try:
                    response = requests.head(url, timeout=10)
                    if response.status_code == 200:
                        print(f"  ✓ Writeup document: OK")
                    else:
                        print(f"  ✗ Writeup document: HTTP {response.status_code}")
                        all_good = False
                except RequestException as e:
                    print(f"  ✗ Writeup document: {e}")
                    all_good = False
            else:
                print(f"  ? Writeup document: Local file ({url})")
        else:
            print(f"  - Writeup document: None")
    
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All project media URLs are accessible!")
    else:
        print("✗ Some project media URLs are not accessible!")
    
    return all_good

if __name__ == '__main__':
    verify_project_media()