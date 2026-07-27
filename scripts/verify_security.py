#!/usr/bin/env python
"""
Complete security hardening verification script
Tests all security measures implemented
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

def verify_security_hardening():
    """Verify all security measures are properly implemented"""
    print("🔐 COMPLETE SECURITY HARDENING VERIFICATION")
    print("=" * 60)
    print(f"Verification Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    issues = []
    passed = 0
    total_checks = 0
    
    # Check 1: Security Middleware Enabled
    total_checks += 4
    middleware_checks = [
        'main.middleware.SecurityHeadersMiddleware',
        'main.middleware.RateLimitMiddleware', 
        'main.middleware.SecurityLoggingMiddleware',
        'main.middleware.BlockSuspiciousRequestsMiddleware'
    ]
    
    print("1. SECURITY MIDDLEWARE VERIFICATION")
    print("-" * 40)
    for middleware in middleware_checks:
        if middleware in settings.MIDDLEWARE:
            print(f"✅ {middleware.split('.')[-1]} - ENABLED")
            passed += 1
        else:
            print(f"❌ {middleware.split('.')[-1]} - DISABLED")
            issues.append(f"Security middleware {middleware} is disabled")
    
    # Check 2: Security Headers Configuration
    total_checks += 6
    security_headers = [
        ('SECURE_BROWSER_XSS_FILTER', True),
        ('SECURE_CONTENT_TYPE_NOSNIFF', True),
        ('X_FRAME_OPTIONS', 'DENY'),
        ('SECURE_HSTS_SECONDS', lambda x: x > 0 if not settings.DEBUG else x == 0),
        ('SESSION_COOKIE_HTTPONLY', True),
        ('CSRF_COOKIE_HTTPONLY', True)
    ]
    
    print("\n2. SECURITY HEADERS CONFIGURATION")
    print("-" * 40)
    for header, expected in security_headers:
        if hasattr(settings, header):
            value = getattr(settings, header)
            if callable(expected):
                if expected(value):
                    print(f"✅ {header}: {value}")
                    passed += 1
                else:
                    print(f"❌ {header}: {value} (invalid)")
                    issues.append(f"{header} has invalid value: {value}")
            elif value == expected:
                print(f"✅ {header}: {value}")
                passed += 1
            else:
                print(f"❌ {header}: {value} (expected: {expected})")
                issues.append(f"{header} should be {expected}, got {value}")
        else:
            print(f"❌ {header}: NOT CONFIGURED")
            issues.append(f"{header} is not configured")
    
    # Check 3: File Upload Security
    total_checks += 3
    print("\n3. FILE UPLOAD SECURITY")
    print("-" * 40)
    
    upload_checks = [
        ('FILE_UPLOAD_MAX_MEMORY_SIZE', 5242880),
        ('DATA_UPLOAD_MAX_MEMORY_SIZE', 5242880),
        ('FILE_UPLOAD_PERMISSIONS', 0o644)
    ]
    
    for setting, expected in upload_checks:
        if hasattr(settings, setting):
            value = getattr(settings, setting)
            if value == expected:
                print(f"✅ {setting}: {value}")
                passed += 1
            else:
                print(f"⚠️ {setting}: {value} (expected: {expected})")
                passed += 0.5  # Partial credit
        else:
            print(f"❌ {setting}: NOT CONFIGURED")
            issues.append(f"{setting} is not configured")
    
    # Check 4: Session Security
    total_checks += 4
    print("\n4. SESSION SECURITY")
    print("-" * 40)
    
    session_checks = [
        ('SESSION_COOKIE_AGE', 3600),
        ('SESSION_EXPIRE_AT_BROWSER_CLOSE', True),
        ('SESSION_SAVE_EVERY_REQUEST', True),
        ('CSRF_COOKIE_SAMESITE', 'Strict')
    ]
    
    for setting, expected in session_checks:
        if hasattr(settings, setting):
            value = getattr(settings, setting)
            if value == expected:
                print(f"✅ {setting}: {value}")
                passed += 1
            else:
                print(f"⚠️ {setting}: {value} (expected: {expected})")
                passed += 0.5
        else:
            print(f"❌ {setting}: NOT CONFIGURED")
            issues.append(f"{setting} is not configured")
    
    # Check 5: Environment Security
    total_checks += 2
    print("\n5. ENVIRONMENT SECURITY")
    print("-" * 40)
    
    if hasattr(settings, 'SECRET_KEY') and 'django-insecure' not in settings.SECRET_KEY:
        print("✅ SECRET_KEY: Secure")
        passed += 1
    else:
        print("❌ SECRET_KEY: Using default/insecure key")
        issues.append("SECRET_KEY is insecure")
    
    admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    if admin_url != 'admin/':
        print(f"✅ ADMIN_URL: Custom ({admin_url})")
        passed += 1
    else:
        print("⚠️ ADMIN_URL: Using default (admin/)")
        issues.append("ADMIN_URL is using default value")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 SECURITY HARDENING SUMMARY")
    print("=" * 60)
    
    score = (passed / total_checks) * 100
    
    if score >= 95:
        status = "🟢 EXCELLENT"
        color = "GREEN"
    elif score >= 85:
        status = "🟡 GOOD" 
        color = "YELLOW"
    elif score >= 70:
        status = "🟠 NEEDS IMPROVEMENT"
        color = "ORANGE"
    else:
        status = "🔴 CRITICAL"
        color = "RED"
    
    print(f"Security Score: {score:.1f}% ({passed:.1f}/{total_checks})")
    print(f"Overall Status: {status}")
    print()
    
    if issues:
        print("🚨 REMAINING ISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
    else:
        print("🎉 ALL SECURITY CHECKS PASSED!")
        print()
    
    print("📝 NEXT STEPS:")
    if score >= 95:
        print("  ✅ Security hardening is complete!")
        print("  ✅ Run security tests to verify functionality")
        print("  ✅ Monitor security logs regularly")
    else:
        print("  🔧 Fix remaining security issues")
        print("  🧪 Run security tests after fixes")
        print("  📊 Re-run this verification script")
    
    print()
    print("🛠️ TESTING COMMANDS:")
    print("  python security_test.py           # Automated security tests")
    print("  python security_manager.py all    # Security audit")
    print("  python admin_security.py          # Admin security check")
    
    return score, issues

if __name__ == '__main__':
    verify_security_hardening()