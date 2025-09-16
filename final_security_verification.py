#!/usr/bin/env python
"""
Final Security Verification Script
"""

import os
import django
import sys
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

def verify_production_security_settings():
    """Verify all production security settings"""
    print("🔐 FINAL SECURITY VERIFICATION")
    print("=" * 50)
    print(f"Verification Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: DEBUG Setting
    print("1. DEBUG SETTING")
    print("-" * 20)
    if settings.DEBUG:
        print("❌ DEBUG is True - Should be False in production")
        return False
    else:
        print("✅ DEBUG is False (Production mode)")
    
    print()
    
    # Test 2: ALLOWED_HOSTS
    print("2. ALLOWED HOSTS")
    print("-" * 20)
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['localhost', '127.0.0.1']:
        print("⚠️  ALLOWED_HOSTS may need production configuration")
    else:
        print(f"✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}")
    
    print()
    
    # Test 3: Secure Cookies
    print("3. SECURE COOKIES")
    print("-" * 20)
    if settings.CSRF_COOKIE_SECURE:
        print("✅ CSRF_COOKIE_SECURE = True")
    else:
        print("❌ CSRF_COOKIE_SECURE should be True")
    
    if settings.SESSION_COOKIE_SECURE:
        print("✅ SESSION_COOKIE_SECURE = True")
    else:
        print("❌ SESSION_COOKIE_SECURE should be True")
    
    print()
    
    # Test 4: HTTPS Redirect
    print("4. HTTPS REDIRECT")
    print("-" * 20)
    if settings.SECURE_SSL_REDIRECT:
        print("✅ SECURE_SSL_REDIRECT = True")
    else:
        print("❌ SECURE_SSL_REDIRECT should be True")
    
    print()
    
    # Test 5: HSTS Configuration
    print("5. HSTS CONFIGURATION")
    print("-" * 20)
    if settings.SECURE_HSTS_SECONDS == 31536000:
        print("✅ HSTS set to 1 year")
    else:
        print(f"❌ HSTS should be 31536000, got {settings.SECURE_HSTS_SECONDS}")
    
    if settings.SECURE_HSTS_INCLUDE_SUBDOMAINS:
        print("✅ HSTS includes subdomains")
    else:
        print("❌ HSTS should include subdomains")
    
    if settings.SECURE_HSTS_PRELOAD:
        print("✅ HSTS preload enabled")
    else:
        print("❌ HSTS preload should be enabled")
    
    print()
    
    # Test 6: Security Headers
    print("6. SECURITY HEADERS")
    print("-" * 20)
    if settings.SECURE_BROWSER_XSS_FILTER:
        print("✅ XSS filter enabled")
    else:
        print("❌ XSS filter should be enabled")
    
    if settings.SECURE_CONTENT_TYPE_NOSNIFF:
        print("✅ Content type sniffing protection enabled")
    else:
        print("❌ Content type sniffing protection should be enabled")
    
    if settings.X_FRAME_OPTIONS == 'DENY':
        print("✅ X-Frame-Options set to DENY")
    else:
        print(f"❌ X-Frame-Options should be 'DENY', got '{settings.X_FRAME_OPTIONS}'")
    
    print()
    
    # Test 7: Middleware
    print("7. SECURITY MIDDLEWARE")
    print("-" * 20)
    required_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.common.CommonMiddleware'
    ]
    
    missing_middleware = []
    for middleware in required_middleware:
        if middleware not in settings.MIDDLEWARE:
            missing_middleware.append(middleware)
    
    if missing_middleware:
        print(f"❌ Missing middleware: {missing_middleware}")
        return False
    else:
        print("✅ All required security middleware enabled")
    
    print()
    
    # Test 8: Custom Security Middleware
    print("8. CUSTOM SECURITY MIDDLEWARE")
    print("-" * 20)
    custom_middleware = [
        'main.middleware.SecurityHeadersMiddleware',
        'main.middleware.RateLimitMiddleware',
        'main.middleware.SecurityLoggingMiddleware',
        'main.middleware.BlockSuspiciousRequestsMiddleware'
    ]
    
    missing_custom_middleware = []
    for middleware in custom_middleware:
        if middleware not in settings.MIDDLEWARE:
            missing_custom_middleware.append(middleware)
    
    if missing_custom_middleware:
        print(f"❌ Missing custom middleware: {missing_custom_middleware}")
    else:
        print("✅ All custom security middleware enabled")
    
    print()
    
    # Test 9: Admin URL
    print("9. ADMIN URL")
    print("-" * 20)
    admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    if admin_url != 'admin/':
        print(f"✅ Custom admin URL: {admin_url}")
    else:
        print("⚠️  Using default admin URL (consider customizing for security)")
    
    print()
    
    # Test 10: Secret Key
    print("10. SECRET KEY")
    print("-" * 20)
    if hasattr(settings, 'SECRET_KEY') and 'django-insecure' not in settings.SECRET_KEY and len(settings.SECRET_KEY) > 32:
        print("✅ Secure SECRET_KEY configured")
    else:
        print("❌ SECRET_KEY needs to be more secure")
    
    print()
    print("=" * 50)
    print("🎉 SECURITY VERIFICATION COMPLETE")
    print()
    print("📋 NEXT STEPS:")
    print("  1. Ensure .env file is properly configured for production")
    print("  2. Run 'python manage.py check --deploy' for additional checks")
    print("  3. Test with automated security scanning tools")
    print("  4. Review and follow the PRODUCTION_SETUP.md guide")
    
    return True

if __name__ == '__main__':
    verify_production_security_settings()