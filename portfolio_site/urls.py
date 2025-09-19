"""
portfolio_site URL Configuration

Secure URL configuration with dynamic admin URL and security headers.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def security_txt(request):
    """Security.txt endpoint for responsible disclosure"""
    content = """Contact: mailto:security@localhost
Expires: 2025-12-31T23:59:59.000Z
Preferred-Languages: en
Policy: https://localhost/security-policy
"""
    return HttpResponse(content.encode('utf-8'), content_type='text/plain')

def robots_txt(request):
    """Robots.txt with security considerations"""
    content = """User-agent: *
Disallow: /admin/
Disallow: /media/private/
Sitemap: https://localhost/sitemap.xml
"""
    return HttpResponse(content.encode('utf-8'), content_type='text/plain')

# Use custom admin URL from settings for security
admin_url = getattr(settings, 'ADMIN_URL', 'admin/')

urlpatterns = [
    # Admin URLs - using secure custom path
    path(admin_url, admin.site.urls),
    
    # Main application URLs
    path('', include('main.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    
    # Security endpoints
    path('.well-known/security.txt', security_txt, name='security_txt'),
    path('security.txt', security_txt, name='security_txt_alt'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

# Serve static files in both development and production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Only serve media files locally when not using Cloudinary
if not hasattr(settings, 'DEFAULT_FILE_STORAGE') or 'cloudinary' not in settings.DEFAULT_FILE_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)