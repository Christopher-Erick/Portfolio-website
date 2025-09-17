#!/usr/bin/env python
"""
Script to check security events, including rate limit violations
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta

def check_rate_limit_events():
    """Check recent rate limit events"""
    try:
        # Import here to ensure Django is set up
        from main.models import SecurityEvent
        
        # Get events from the last hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        rate_limit_events = SecurityEvent.objects.filter(
            event_type='rate_limit',
            created_at__gte=one_hour_ago
        ).order_by('-created_at')
        
        print("📊 Rate Limit Events (Last Hour)")
        print("=" * 35)
        
        if rate_limit_events.exists():
            for event in rate_limit_events:
                print(f"⏰ {event.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                print(f"📍 IP: {event.ip_address}")
                print(f"📝 Description: {event.description}")
                print(f"🔗 Path: {event.path}")
                print(f"🔧 Method: {event.method}")
                print("-" * 30)
        else:
            print("✅ No rate limit events found in the last hour")
            
    except Exception as e:
        print(f"❌ Error checking rate limit events: {e}")

def check_all_recent_events():
    """Check all recent security events"""
    try:
        # Import here to ensure Django is set up
        from main.models import SecurityEvent
        
        # Get events from the last hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent_events = SecurityEvent.objects.filter(
            created_at__gte=one_hour_ago
        ).order_by('-created_at')[:20]  # Limit to 20 most recent
        
        print("📊 Recent Security Events (Last Hour)")
        print("=" * 35)
        
        event_type_labels = {
            'login_failed': 'Failed Login',
            'login_success': 'Successful Login',
            'admin_access': 'Admin Access',
            'contact_submission': 'Contact Submission',
            'rate_limit': 'Rate Limit Violation',
            'suspicious_request': 'Suspicious Request',
            'file_upload': 'File Upload',
            'security_scan': 'Security Scan Detected',
        }
        
        if recent_events.exists():
            for event in recent_events:
                event_label = event_type_labels.get(event.event_type, event.get_event_type_display())
                print(f"⏰ {event.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                print(f"📍 IP: {event.ip_address}")
                print(f"🏷️  Type: {event_label}")
                print(f"📈 Severity: {event.get_severity_display()}")
                print(f"📝 Description: {event.description}")
                print(f"🔗 Path: {event.path}")
                print("-" * 30)
        else:
            print("✅ No security events found in the last hour")
            
    except Exception as e:
        print(f"❌ Error checking security events: {e}")

def check_failed_logins():
    """Check recent failed login attempts"""
    try:
        # Import here to ensure Django is set up
        from main.models import SecurityEvent
        
        # Get failed login events from the last hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        failed_logins = SecurityEvent.objects.filter(
            event_type='login_failed',
            created_at__gte=one_hour_ago
        ).order_by('-created_at')
        
        print("🔐 Failed Login Attempts (Last Hour)")
        print("=" * 35)
        
        if failed_logins.exists():
            for event in failed_logins:
                print(f"⏰ {event.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                print(f"📍 IP: {event.ip_address}")
                print(f"👤 Username: {event.username}")
                print(f"📝 Description: {event.description}")
                print("-" * 30)
        else:
            print("✅ No failed login attempts found in the last hour")
            
    except Exception as e:
        print(f"❌ Error checking failed login attempts: {e}")

if __name__ == '__main__':
    print("🛡️  Security Events Checker")
    print("=" * 25)
    print()
    
    check_rate_limit_events()
    print()
    
    check_failed_logins()
    print()
    
    check_all_recent_events()