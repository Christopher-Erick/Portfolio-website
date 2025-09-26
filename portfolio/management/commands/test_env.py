import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = 'Test environment variables in management command'

    def handle(self, *args, **options):
        # Load environment variables from .env file
        project_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = project_dir / '.env'
        self.stdout.write(f'Looking for .env file at: {env_file}')
        self.stdout.write(f'.env file exists: {env_file.exists()}')
        
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                        self.stdout.write(f'Loaded {key.strip()} = {value.strip()}')
        
        # Print Cloudinary settings
        self.stdout.write(f"DEBUG: {getattr(settings, 'DEBUG', 'Not set')}")
        self.stdout.write(f"CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'Not set')}")
        self.stdout.write(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
        
        # Check if Cloudinary is configured
        if not hasattr(settings, 'DEFAULT_FILE_STORAGE') or 'cloudinary' not in settings.DEFAULT_FILE_STORAGE:
            self.stdout.write(
                'Cloudinary is not configured.'
            )
        else:
            self.stdout.write(
                'Cloudinary is configured!'
            )