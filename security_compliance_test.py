#!/usr/bin/env python
"""
Security compliance test to verify production settings
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
from django.test import TestCase, override_settings

class SecurityComplianceTest(TestCase):
    """Test security compliance for production deployment"""
    
    def test_debug_disabled_in_production(self):
        """Test that DEBUG is False in production"""
        # In production, DEBUG should be False
        if not os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes'):
            self.assertFalse(settings.DEBUG, "DEBUG should be False in production")
        print(f"✅ DEBUG setting: {settings.DEBUG}")
    
    def test_allowed_hosts_configured(self):
        """Test that ALLOWED_HOSTS is properly configured"""
        self.assertTrue(len(settings.ALLOWED_HOSTS) > 0, "ALLOWED_HOSTS should not be empty")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    def test_secure_cookies_enabled(self):
        """Test that secure cookies are enabled in production"""
        if not settings.DEBUG:
            self.assertTrue(settings.SESSION_COOKIE_SECURE, "SESSION_COOKIE_SECURE should be True in production")
            self.assertTrue(settings.CSRF_COOKIE_SECURE, "CSRF_COOKIE_SECURE should be True in production")
            print("✅ Secure cookies enabled")
        else:
            print("⚠️ Secure cookies test skipped (DEBUG mode)")
    
    def test_https_redirect_enabled(self):
        """Test that HTTPS redirect is enabled in production"""
        if not settings.DEBUG:
            self.assertTrue(settings.SECURE_SSL_REDIRECT, "SECURE_SSL_REDIRECT should be True in production")
            print("✅ HTTPS redirect enabled")
        else:
            print("⚠️ HTTPS redirect test skipped (DEBUG mode)")
    
    def test_security_middleware_enabled(self):
        """Test that security middleware is enabled"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.common.CommonMiddleware',
            'main.middleware.SecurityHeadersMiddleware',
            'main.middleware.RateLimitMiddleware',
            'main.middleware.SecurityLoggingMiddleware',
            'main.middleware.BlockSuspiciousRequestsMiddleware',
        ]
        
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE, f"Missing middleware: {middleware}")
        
        print("✅ All security middleware enabled")
    
    def test_hsts_configuration(self):
        """Test HSTS configuration"""
        if not settings.DEBUG:
            self.assertEqual(settings.SECURE_HSTS_SECONDS, 31536000, "HSTS should be set to 1 year")
            self.assertTrue(settings.SECURE_HSTS_INCLUDE_SUBDOMAINS, "HSTS should include subdomains")
            self.assertTrue(settings.SECURE_HSTS_PRELOAD, "HSTS should support preload")
            print("✅ HSTS properly configured")
        else:
            print("⚠️ HSTS test skipped (DEBUG mode)")
    
    def test_security_headers(self):
        """Test security headers configuration"""
        self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER, "XSS filter should be enabled")
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF, "Content type sniffing protection should be enabled")
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY', "X-Frame-Options should be DENY")
        print("✅ Security headers configured")
    
    def test_file_upload_security(self):
        """Test file upload security settings"""
        self.assertEqual(settings.FILE_UPLOAD_MAX_MEMORY_SIZE, 5242880, "File upload size should be limited")
        self.assertEqual(settings.DATA_UPLOAD_MAX_MEMORY_SIZE, 5242880, "Data upload size should be limited")
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644, "File upload permissions should be restricted")
        print("✅ File upload security configured")
    
    def test_admin_url_customization(self):
        """Test that admin URL is customized"""
        admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
        self.assertNotEqual(admin_url, 'admin/', "Admin URL should be customized for security")
        print(f"✅ Custom admin URL: {admin_url}")

def run_security_tests():
    """Run all security compliance tests"""
    print("🔐 SECURITY COMPLIANCE TEST")
    print("=" * 50)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_instance = SecurityComplianceTest()
    
    # Run all test methods
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    total = len(test_methods)
    
    for method_name in test_methods:
        try:
            method = getattr(test_instance, method_name)
            method()
            passed += 1
            print(f"✅ {method_name.replace('test_', '').replace('_', ' ').title()}")
        except Exception as e:
            print(f"❌ {method_name.replace('test_', '').replace('_', ' ').title()}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Security Compliance Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL SECURITY COMPLIANCE TESTS PASSED!")
        print("\n✅ Your Django application is properly configured for production security.")
    else:
        print("⚠️ Some security compliance tests failed.")
        print("Please review the failed tests and fix the issues before deployment.")
    
    return passed == total

if __name__ == '__main__':
    run_security_tests()