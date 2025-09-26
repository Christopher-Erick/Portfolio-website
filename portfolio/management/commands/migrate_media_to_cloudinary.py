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
            self.stdout.write(f'Processing project: {project.title}')
            
            # Check if project has featured image
            if project.featured_image and project.featured_image.name:
                old_path = str(project.featured_image)
                self.stdout.write(f'  Featured image: {old_path}')
                
                # Only migrate if it's a local path (not already in Cloudinary)
                if not old_path.startswith('http'):
                    try:
                        # Clear the current file reference
                        project.featured_image = None
                        project.save()
                        
                        # Re-save the project to trigger Cloudinary upload
                        project.save()
                        
                        if project.featured_image:
                            new_path = str(project.featured_image)
                            migrated_count += 1
                            self.stdout.write(
                                f'  Successfully migrated featured image to: {new_path}'
                            )
                        else:
                            self.stdout.write(
                                f'  Failed to migrate featured image'
                            )
                    except Exception as e:
                        self.stdout.write(
                            f'  Failed to migrate featured image: {str(e)}'
                        )
                else:
                    self.stdout.write(
                        f'  Featured image already in Cloudinary: {old_path}'
                    )
            
            # Check if project has writeup document
            if project.writeup_document and project.writeup_document.name:
                old_path = str(project.writeup_document)
                self.stdout.write(f'  Writeup document: {old_path}')
                
                # Only migrate if it's a local path (not already in Cloudinary)
                if not old_path.startswith('http'):
                    try:
                        # Clear the current file reference
                        project.writeup_document = None
                        project.save()
                        
                        # Re-save the project to trigger Cloudinary upload
                        project.save()
                        
                        if project.writeup_document:
                            new_path = str(project.writeup_document)
                            migrated_count += 1
                            self.stdout.write(
                                f'  Successfully migrated writeup document to: {new_path}'
                            )
                        else:
                            self.stdout.write(
                                f'  Failed to migrate writeup document'
                            )
                    except Exception as e:
                        self.stdout.write(
                            f'  Failed to migrate writeup document: {str(e)}'
                        )
                else:
                    self.stdout.write(
                        f'  Writeup document already in Cloudinary: {old_path}'
                    )
        
        self.stdout.write(
            f'Successfully migrated {migrated_count} files to Cloudinary'
        )