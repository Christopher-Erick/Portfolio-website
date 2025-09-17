from django.core.management.base import BaseCommand
from django.http import HttpRequest
from main.context_processors import personal_info

class Command(BaseCommand):
    help = 'Test context processor values'

    def handle(self, *args, **options):
        # Create a mock request
        request = HttpRequest()
        
        # Get context data
        context_data = personal_info(request)
        
        self.stdout.write("Context Processor Values:")
        self.stdout.write("=" * 30)
        for key, value in context_data.items():
            self.stdout.write(f"{key}: {value}")