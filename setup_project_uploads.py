#!/usr/bin/env python
"""
Instructions and helper script for uploading project images and writeups
"""
import os
import sys
import django
from config import AdminConfig

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.contrib.auth.models import User
from portfolio.models import Project


def create_superuser_if_needed():
    """Create a superuser for Django admin access"""
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser for Django admin...")
        User.objects.create_superuser(
            username=AdminConfig.get_admin_username(),
            email=AdminConfig.get_admin_email(),
            password=input('Enter admin password: ') or 'changeme123'
        )
        print("Superuser created! Username: admin, Password: [Hidden for security]")
    else:
        print("Superuser already exists.")


def show_upload_instructions():
    """Show instructions for uploading project assets"""
    print("\n" + "="*60)
    print("PROJECT ASSET UPLOAD INSTRUCTIONS")
    print("="*60)
    
    print("\n1. ACCESS DJANGO ADMIN:")
    print("   - Go to: http://127.0.0.1:8000/admin/")
    print("   - Login with: admin / [use the password you set]")
    
    print("\n2. UPLOAD PROJECT IMAGE:")
    print("   - Navigate to: Portfolio > Projects")
    print("   - Click on 'Comprehensive Security Assessment Methodology Study'")
    print("   - In the 'Media' section:")
    print("     * Click 'Choose File' next to 'Featured image'")
    print("     * Upload your Vulnerability Assessment image")
    
    print("\n3. UPLOAD PROJECT WRITEUP:")
    print("   - In the same project edit page:")
    print("     * Click 'Choose File' next to 'Writeup document'")
    print("     * Upload your writeup (PDF, DOC, DOCX)")
    
    print("\n4. SAVE THE PROJECT:")
    print("   - Click 'Save' at the bottom of the page")
    
    print("\n5. VIEW YOUR PROJECT:")
    print("   - Go to: http://127.0.0.1:8000/portfolio/")
    print("   - Click on your project to see the image and writeup link")
    
    print("\n" + "="*60)
    print("SUPPORTED FILE FORMATS:")
    print("="*60)
    print("Images: JPG, PNG, GIF, WEBP")
    print("Documents: PDF, DOC, DOCX, TXT")
    print("="*60)


def main():
    print("Setting up project asset upload system...")
    
    # Create superuser if needed
    create_superuser_if_needed()
    
    # Show upload instructions
    show_upload_instructions()
    
    # Show current project status
    project = Project.objects.filter(slug='security-assessment-methodology-study').first()
    if project:
        print(f"\nCurrent project status:")
        print(f"- Title: {project.title}")
        print(f"- Featured Image: {'✓ Uploaded' if project.featured_image else '✗ Not uploaded'}")
        print(f"- Writeup Document: {'✓ Uploaded' if project.writeup_document else '✗ Not uploaded'}")
    
    print(f"\nDjango server should be running at: http://127.0.0.1:8000/")
    print(f"Django admin available at: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    main()