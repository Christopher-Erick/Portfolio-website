import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.conf import settings
if 'localhost' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('localhost')
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import RequestFactory
from main.views import home

def export_site():
    factory = RequestFactory()
    request = factory.get('/', HTTP_HOST='localhost')
    
    try:
        response = home(request)
        html_content = response.content.decode('utf-8')
    except Exception as e:
        print(f"Warning/Error rendering home view: {e}")
        # Fallback to render template directly if view encounters issues
        from django.template.loader import render_to_string
        html_content = render_to_string('main/home.html', {'testimonials': []}, request=request)
    
    output_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
    os.makedirs(output_dir, exist_ok=True)
    
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Successfully generated static {index_path}")

if __name__ == '__main__':
    export_site()
