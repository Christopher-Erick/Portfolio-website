import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project
from pathlib import Path

class Command(BaseCommand):
    help = 'Update Cloudinary URLs for existing projects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            type=str,
            default='projects',
            help='Base folder name in Cloudinary (default: projects)'
        )
        parser.add_argument(
            '--writeup-folder',
            type=str,
            default='writeups',
            help='Folder name for writeups in Cloudinary (default: writeups)'
        )
        parser.add_argument(
            '--image-folder',
            type=str,
            default='writeupsimages',
            help='Folder name for writeup images in Cloudinary (default: writeupsimages)'
        )

    def handle(self, *args, **options):
        # Load environment variables from .env file
        project_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = project_dir / '.env'
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        # Check if Cloudinary is configured
        if not hasattr(settings, 'DEFAULT_FILE_STORAGE') or 'cloudinary' not in settings.DEFAULT_FILE_STORAGE:
            self.stdout.write(
                'Cloudinary is not configured. Please set up Cloudinary environment variables.'
            )
            return

        # Import Cloudinary
        try:
            import cloudinary
            import cloudinary.api
            import cloudinary.uploader
        except ImportError:
            self.stdout.write(
                'Cloudinary packages not installed. Please install django-cloudinary-storage.'
            )
            return

        # Get Cloudinary configuration
        cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
        if not cloud_name:
            self.stdout.write(
                'CLOUDINARY_CLOUD_NAME is not set in environment variables.'
            )
            return

        self.stdout.write(
            f'Cloudinary is configured for cloud: {cloud_name}'
        )

        # Get all projects
        projects = getattr(Project, 'objects').all()
        
        updated_count = 0
        
        for project in projects:
            self.stdout.write(f'Processing project: {project.title}')
            
            # Handle featured images
            if project.featured_image and project.featured_image.name:
                old_path = str(project.featured_image)
                self.stdout.write(f'  Current featured image: {old_path}')
                
                # If it's a local path, we need to update it
                if not old_path.startswith('http'):
                    # Construct the new Cloudinary URL
                    # Assuming your images are in the writeupsimages folder
                    filename = os.path.basename(old_path)
                    new_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{options['image_folder']}/{filename}"
                    
                    # Update the field directly
                    project.featured_image.name = new_url
                    project.save(update_fields=['featured_image'])
                    
                    updated_count += 1
                    self.stdout.write(
                        f'  Updated featured image to: {new_url}'
                    )
            
            # Handle writeup documents
            if project.writeup_document and project.writeup_document.name:
                old_path = str(project.writeup_document)
                self.stdout.write(f'  Current writeup document: {old_path}')
                
                # If it's a local path, we need to update it
                if not old_path.startswith('http'):
                    # Construct the new Cloudinary URL
                    # Assuming your documents are in the writeups folder
                    filename = os.path.basename(old_path)
                    new_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{options['writeup_folder']}/{filename}"
                    
                    # Update the field directly
                    project.writeup_document.name = new_url
                    project.save(update_fields=['writeup_document'])
                    
                    updated_count += 1
                    self.stdout.write(
                        f'  Updated writeup document to: {new_url}'
                    )
        
        self.stdout.write(
            f'Successfully updated {updated_count} file URLs to Cloudinary'
        )