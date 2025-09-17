import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

# Setup Django
django.setup()

# Import the view
from main.views import health_check
from django.http import HttpRequest

# Create a mock request
request = HttpRequest()
request.method = 'GET'

# Call the view
try:
    response = health_check(request)
    print(f"Response status code: {response.status_code}")
    print(f"Response content length: {len(response.content)}")
    print("Health check view is working correctly!")
except Exception as e:
    print(f"Error in health check view: {e}")
    import traceback
    traceback.print_exc()