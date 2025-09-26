#!/usr/bin/env python
"""
Post-deployment script to populate database with initial data
This script should be run after deployment to ensure the database has all necessary data
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.core.management import execute_from_command_line
from populate_all_data import main as populate_data


def update_database_with_cloudinary_urls():
    """Update database with Cloudinary URLs after deployment"""
    print("🔗 Updating database with Cloudinary URLs...")
    
    try:
        from portfolio.models import Project
        
        # Mapping of local file paths to Cloudinary URLs
        # Images mapping
        image_mapping = {
            "projects/VULNERABILITY_ASSEMEMENT.PNG": "https://res.cloudinary.com/dge5xurfz/image/upload/v1758913083/writeupsimages/VULNERABILITY_ASSEMEMENT",
            "projects/splunk.png": "https://res.cloudinary.com/dge5xurfz/image/upload/v1758913069/writeupsimages/splunk",
            "projects/malware.PNG": "https://res.cloudinary.com/dge5xurfz/image/upload/v1758913060/writeupsimages/malware"
        }
        
        # Documents mapping (raw files)
        document_mapping = {
            "projects/writeups/SECURITY_ASSESSEMENT.pdf": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914162/writeups_raw/SECURITY_ASSESSEMENT.pdf",
            "projects/writeups/Splunk_Exploring_SPL.pdf": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914165/writeups_raw/Splunk_Exploring_SPL.pdf",
            "projects/writeups/Malware_Analysis.pdf": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914110/writeups_raw/Malware_Analysis.pdf"
        }
        
        # Get all projects
        projects = getattr(Project, 'objects').all()
        
        updated_count = 0
        
        for project in projects:
            print(f"  Processing project: {project.title}")
            needs_save = False
            
            # Update featured image if it's a local path
            if project.featured_image and project.featured_image.name:
                current_image = str(project.featured_image)
                if not current_image.startswith('http'):
                    # Look for matching local path
                    for local_path, cloudinary_url in image_mapping.items():
                        if local_path in current_image or local_path.split('/')[-1] in current_image:
                            print(f"    Updating featured image: {current_image} -> {cloudinary_url}")
                            project.featured_image.name = cloudinary_url
                            needs_save = True
                            updated_count += 1
                            break
            
            # Update writeup document if it's a local path
            if project.writeup_document and project.writeup_document.name:
                current_document = str(project.writeup_document)
                if not current_document.startswith('http'):
                    # Look for matching local path
                    for local_path, cloudinary_url in document_mapping.items():
                        if local_path in current_document or local_path.split('/')[-1] in current_document:
                            print(f"    Updating writeup document: {current_document} -> {cloudinary_url}")
                            project.writeup_document.name = cloudinary_url
                            needs_save = True
                            updated_count += 1
                            break
            
            # Save the project if any fields were updated
            if needs_save:
                project.save(update_fields=['featured_image', 'writeup_document'])
                print(f"    Project updated successfully")
        
        print(f"🔗 Database update completed! Updated {updated_count} file references.")
        
    except Exception as e:
        print(f"❌ Error updating Cloudinary URLs: {e}")


def run_post_deploy():
    """Run post-deployment tasks"""
    print("🚀 Running post-deployment tasks...")
    
    try:
        # Run migrations to ensure database schema is up to date
        print("🔧 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Populate data
        print("📊 Populating database with initial data...")
        populate_data()
        
        # Update database with Cloudinary URLs
        print("🔗 Updating database with Cloudinary URLs...")
        update_database_with_cloudinary_urls()
        
        print("✅ Post-deployment tasks completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during post-deployment: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_post_deploy()