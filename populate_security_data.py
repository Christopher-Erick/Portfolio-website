#!/usr/bin/env python
"""
Populate security dashboard with test data
"""
import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import SecurityEvent
from django.utils import timezone


def create_test_security_events():
    """Create test security events for dashboard demonstration"""
    print("🔧 Creating test security events...")
    
    now = timezone.now()
    
    # Test events from the last 24 hours
    test_events = [
        {
            'event_type': 'admin_access',
            'severity': 'low',
            'ip_address': '127.0.0.1',
            'username': 'portfolio_admin_8l1e21',
            'description': 'Admin panel access',
            'path': '/secure-admin-ceo789/',
            'method': 'GET',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': now - timedelta(minutes=30)
        },
        {
            'event_type': 'contact_submission',
            'severity': 'low',
            'ip_address': '192.168.1.100',
            'username': '',
            'description': 'Contact form submission from Test User (test@example.com)',
            'path': '/contact/',
            'method': 'POST',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': now - timedelta(hours=2)
        },
        {
            'event_type': 'suspicious_request',
            'severity': 'medium',
            'ip_address': '45.76.123.45',
            'username': '',
            'description': 'Suspicious pattern detected: <script',
            'path': '/search/?q=<script>alert("xss")</script>',
            'method': 'GET',
            'user_agent': 'curl/7.68.0',
            'created_at': now - timedelta(hours=3)
        },
        {
            'event_type': 'rate_limit',
            'severity': 'medium',
            'ip_address': '87.249.134.15',
            'username': '',
            'description': 'Rate limit exceeded on /contact/ (11/10 requests)',
            'path': '/contact/',
            'method': 'POST',
            'user_agent': 'python-requests/2.28.1',
            'created_at': now - timedelta(hours=4)
        },
        {
            'event_type': 'security_scan',
            'severity': 'high',
            'ip_address': '198.51.100.42',
            'username': '',
            'description': 'Malicious user agent detected: nikto',
            'path': '/admin/',
            'method': 'GET',
            'user_agent': 'Nikto/2.1.6',
            'created_at': now - timedelta(hours=6)
        },
        {
            'event_type': 'login_failed',
            'severity': 'medium',
            'ip_address': '203.0.113.195',
            'username': 'admin',
            'description': 'Failed login attempt for username: admin',
            'path': '/secure-admin-ceo789/login/',
            'method': 'POST',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'created_at': now - timedelta(hours=8)
        },
        {
            'event_type': 'login_failed',
            'severity': 'medium',
            'ip_address': '203.0.113.195',
            'username': 'administrator',
            'description': 'Failed login attempt for username: administrator',
            'path': '/secure-admin-ceo789/login/',
            'method': 'POST',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'created_at': now - timedelta(hours=8, minutes=5)
        },
        {
            'event_type': 'contact_submission',
            'severity': 'low',
            'ip_address': '172.16.0.50',
            'username': '',
            'description': 'Contact form submission from Jane Doe (jane@company.com)',
            'path': '/contact/',
            'method': 'POST',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'created_at': now - timedelta(hours=12)
        },
    ]
    
    created_count = 0
    for event_data in test_events:
        created_at = event_data.pop('created_at')
        event = SecurityEvent.objects.create(**event_data)
        event.created_at = created_at
        event.save()
        created_count += 1
    
    print(f"✅ Created {created_count} test security events")
    print("📊 Security dashboard is now populated with realistic data")
    print("\n🔗 Access the security dashboard at:")
    print("   http://127.0.0.1:8000/security-dashboard/")
    print("\n🔑 Admin panel:")
    print("   http://127.0.0.1:8000/secure-admin-ceo789/")


if __name__ == '__main__':
    create_test_security_events()