import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project

class Command(BaseCommand):
    help = 'Migrate existing media files to Cloudinary'

    def handle(self, *args, **options):
        # Check if Cloudinary is configured
        if not hasattr(settings, 'DEFAULT_FILE_STORAGE') or 'cloudinary' not in settings.DEFAULT_FILE_STORAGE:
            self.stdout.write(
                'Cloudinary is not configured. Please set up Cloudinary environment variables.'
            )
            return

        # Import Cloudinary
        try:
            import cloudinary
            import cloudinary.uploader
        except ImportError:
            self.stdout.write(
                'Cloudinary packages not installed. Please install django-cloudinary-storage.'
            )
            return

        self.stdout.write(
            'Cloudinary is configured. Starting migration...'
        )

        # Get all projects
        projects = getattr(Project, 'objects').all()
        
        migrated_count = 0
        
        for project in projects:
            # Check if project has featured image
            if project.featured_image:
                old_path = project.featured_image.path if hasattr(project.featured_image, 'path') else str(project.featured_image)
                self.stdout.write(f'Project: {project.title}')
                self.stdout.write(f'  Featured image: {old_path}')
                
                # Try to migrate the file
                try:
                    # Re-save the project to trigger Cloudinary upload
                    project.save()
                    migrated_count += 1
                    self.stdout.write(
                        f'  Successfully migrated featured image'
                    )
                except Exception as e:
                    self.stdout.write(
                        f'  Failed to migrate featured image: {str(e)}'
                    )
            
            # Check if project has writeup document
            if project.writeup_document:
                old_path = project.writeup_document.path if hasattr(project.writeup_document, 'path') else str(project.writeup_document)
                self.stdout.write(f'  Writeup document: {old_path}')
                
                # Try to migrate the file
                try:
                    # Re-save the project to trigger Cloudinary upload
                    project.save()
                    migrated_count += 1
                    self.stdout.write(
                        f'  Successfully migrated writeup document'
                    )
                except Exception as e:
                    self.stdout.write(
                        f'  Failed to migrate writeup document: {str(e)}'
                    )
        
        self.stdout.write(
            f'Successfully migrated {migrated_count} files to Cloudinary'
        )