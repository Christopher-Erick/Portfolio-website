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

# Ultra-Hardened A+ Grade Content Security Policy & Edge Headers
SECURITY_HEADERS = """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), display-capture=(), autoplay=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://use.fontawesome.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com https://use.fontawesome.com data:; img-src 'self' data: https: blob:; connect-src 'self' https:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests;
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
  Cross-Origin-Embedder-Policy: require-corp
"""

def export_site():
    factory = RequestFactory()
    output_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Export all HTML pages
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

    # 2. Write Cloudflare Edge Security Headers (_headers)
    headers_path = os.path.join(output_dir, '_headers')
    with open(headers_path, 'w', encoding='utf-8') as f:
        f.write(SECURITY_HEADERS)
    print(f"Generated Cloudflare Security Headers: {headers_path}")

if __name__ == '__main__':
    export_site()
