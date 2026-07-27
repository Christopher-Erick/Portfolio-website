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
from main.views import home, about, resume, contact
from portfolio.views import portfolio_list
from blog.views import blog_list

PAGES_TO_EXPORT = [
    ('/', 'index.html', home),
    ('/about/', 'about/index.html', about),
    ('/resume/', 'resume/index.html', resume),
    ('/contact/', 'contact/index.html', contact),
    ('/portfolio/', 'portfolio/index.html', portfolio_list),
    ('/blog/', 'blog/index.html', blog_list),
]

def export_site():
    factory = RequestFactory()
    output_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
    os.makedirs(output_dir, exist_ok=True)
    
    for path, relative_file, view_func in PAGES_TO_EXPORT:
        request = factory.get(path, HTTP_HOST='localhost')
        try:
            response = view_func(request)
            html_content = response.content.decode('utf-8')
        except Exception as e:
            print(f"Warning rendering {path}: {e}")
            from django.template.loader import render_to_string
            try:
                html_content = render_to_string('main/home.html', {}, request=request)
            except Exception:
                html_content = f"<html><body><h1>Page: {path}</h1></body></html>"
        
        # Replace /static/ with / so assets load from root on Cloudflare Pages
        html_content = html_content.replace('/static/', '/')
        
        target_path = os.path.join(output_dir, relative_file.replace('/', os.sep))
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Generated static page: {target_path}")

if __name__ == '__main__':
    export_site()
