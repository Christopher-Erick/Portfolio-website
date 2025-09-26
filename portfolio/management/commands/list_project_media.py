import os
import django
from django.core.management.base import BaseCommand
from portfolio.models import Project

class Command(BaseCommand):
    help = 'List all projects and their media file status'

    def handle(self, *args, **options):
        # Get all projects
        projects = getattr(Project, 'objects').all()
        
        if not projects:
            self.stdout.write('No projects found in the database.')
            return
            
        self.stdout.write(f'Found {projects.count()} projects:')
        self.stdout.write('=' * 80)
        
        for project in projects:
            self.stdout.write(f'\nProject: {project.title}')
            self.stdout.write(f'  Slug: {project.slug}')
            
            # Check featured image
            if project.featured_image and project.featured_image.name:
                image_path = str(project.featured_image)
                if image_path.startswith('http'):
                    self.stdout.write(f'  Featured Image: {image_path} (Cloudinary)')
                else:
                    self.stdout.write(f'  Featured Image: {image_path} (Local)')
            else:
                self.stdout.write('  Featured Image: None')
            
            # Check writeup document
            if project.writeup_document and project.writeup_document.name:
                doc_path = str(project.writeup_document)
                if doc_path.startswith('http'):
                    self.stdout.write(f'  Writeup Document: {doc_path} (Cloudinary)')
                else:
                    self.stdout.write(f'  Writeup Document: {doc_path} (Local)')
            else:
                self.stdout.write('  Writeup Document: None')
                
            self.stdout.write('-' * 40)