#!/usr/bin/env python
"""
Simple script to help with rate limit issues
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

def get_help_info():
    """Print help information about rate limits"""
    print("🛡️  Rate Limit Information")
    print("=" * 25)
    print()
    print("Your Django application has the following rate limits:")
    print()
    print("1. Admin Panel: 50 requests per 5 minutes")
    print("2. Contact Form: 10 requests per 15 minutes")
    print("3. General Pages: 200 requests per 5 minutes")
    print()
    print("If you're seeing 'Rate limit exceeded' messages, it means")
    print("you've made too many requests in a short period of time.")
    print()
    print("Solutions:")
    print("1. Wait for the rate limit window to expire (5-15 minutes)")
    print("2. If you have Render console access, clear the cache:")
    print("   python manage.py shell -c \"from django.core.cache import cache; cache.clear()\"")
    print("3. Try accessing from a different IP address")
    print()
    print("For more detailed information about what triggered the rate limit,")
    print("check the Security Dashboard in your admin panel.")

if __name__ == '__main__':
    get_help_info()