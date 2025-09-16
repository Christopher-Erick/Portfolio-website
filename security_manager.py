#!/usr/bin/env python
"""
Security management script for portfolio application
Performs security checks and generates reports
"""

import os
import sys
import django
from datetime import datetime, timedelta
import re

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from main.models import ContactSubmission


def security_check():
    """Perform comprehensive security checks"""
    print("🔒 SECURITY AUDIT REPORT")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    issues = []
    
    # Check 1: DEBUG mode
    if settings.DEBUG:
        issues.append("❌ DEBUG mode is enabled (security risk in production)")
    else:
        print("✅ DEBUG mode is disabled")
    
    # Check 2: Secret key
    if 'django-insecure' in settings.SECRET_KEY:
        issues.append("❌ Using default/insecure SECRET_KEY")
    else:
        print("✅ SECRET_KEY appears to be secure")
    
    # Check 3: ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS and not settings.DEBUG:
        issues.append("❌ ALLOWED_HOSTS is empty")
    else:
        print("✅ ALLOWED_HOSTS is configured")
    
    # Check 4: HTTPS settings
    if hasattr(settings, 'SECURE_SSL_REDIRECT') and settings.SECURE_SSL_REDIRECT:
        print("✅ HTTPS redirect is enabled")
    else:
        if not settings.DEBUG:
            issues.append("❌ HTTPS redirect not configured")
    
    # Check 5: Security headers
    required_headers = [
        'SECURE_BROWSER_XSS_FILTER',
        'SECURE_CONTENT_TYPE_NOSNIFF',
        'X_FRAME_OPTIONS'
    ]
    
    for header in required_headers:
        if hasattr(settings, header):
            print(f"✅ {header} is configured")
        else:
            issues.append(f"❌ {header} not configured")
    
    # Check 6: Admin URL
    admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    if admin_url == 'admin/':
        issues.append("❌ Using default admin URL (security risk)")
    else:
        print("✅ Custom admin URL is configured")
    
    # Check 7: File upload limits
    if hasattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE'):
        print("✅ File upload limits are configured")
    else:
        issues.append("❌ File upload limits not configured")
    
    print()
    
    if issues:
        print("🚨 SECURITY ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ No major security issues found!")
    
    print()
    return len(issues)


def check_suspicious_activity():
    """Check for suspicious contact form submissions"""
    print("🕵️ SUSPICIOUS ACTIVITY CHECK")
    print("=" * 50)
    
    # Check recent submissions
    recent_submissions = ContactSubmission.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).order_by('-created_at')
    
    suspicious_count = 0
    
    for submission in recent_submissions:
        # Check for suspicious patterns
        content = f"{submission.name} {submission.email} {submission.subject} {submission.message}".lower()
        
        suspicious_patterns = [
            r'<script',  # XSS attempts
            r'union\s+select',  # SQL injection
            r'viagra',  # Spam
            r'casino',  # Spam
            r'lottery',  # Spam
            r'winner',  # Spam
            r'http[s]?://(?!localhost)',  # External links
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content):
                print(f"⚠️  Suspicious submission from {submission.email}: {pattern}")
                suspicious_count += 1
                break
    
    if suspicious_count == 0:
        print("✅ No suspicious submissions found in the last 7 days")
    else:
        print(f"🚨 Found {suspicious_count} potentially suspicious submissions")
    
    print()


def generate_security_report():
    """Generate a comprehensive security report"""
    print("📊 GENERATING SECURITY REPORT")
    print("=" * 50)
    
    with open('security_report.txt', 'w') as f:
        f.write("PORTFOLIO SECURITY REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Security configuration summary
        f.write("SECURITY CONFIGURATION:\n")
        f.write(f"- DEBUG: {settings.DEBUG}\n")
        f.write(f"- ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}\n")
        f.write(f"- ADMIN_URL: {getattr(settings, 'ADMIN_URL', 'admin/')}\n")
        f.write(f"- SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', False)}\n")
        f.write(f"- SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', False)}\n")
        f.write(f"- CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', False)}\n\n")
        
        # Recent activity
        f.write("RECENT ACTIVITY:\n")
        recent_submissions = ContactSubmission.objects.filter(
            created_at__gte=datetime.now() - timedelta(days=30)
        ).count()
        f.write(f"- Contact submissions (last 30 days): {recent_submissions}\n")
        
        f.write("\nFor detailed logs, check:\n")
        f.write("- logs/django.log\n")
        f.write("- logs/security.log\n")
    
    print("✅ Security report generated: security_report.txt")


def main():
    """Main security management function"""
    if len(sys.argv) < 2:
        print("Usage: python security_manager.py [check|activity|report|all]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'check':
        security_check()
    elif command == 'activity':
        check_suspicious_activity()
    elif command == 'report':
        generate_security_report()
    elif command == 'all':
        issues = security_check()
        check_suspicious_activity()
        generate_security_report()
        
        print("🎯 SUMMARY")
        print("=" * 50)
        if issues == 0:
            print("✅ System security status: GOOD")
        elif issues <= 2:
            print("⚠️  System security status: NEEDS ATTENTION")
        else:
            print("🚨 System security status: CRITICAL - IMMEDIATE ACTION REQUIRED")
    else:
        print("Invalid command. Use: check, activity, report, or all")


if __name__ == '__main__':
    main()