#!/usr/bin/env python
"""
Script to find the correct admin URL for your deployed application
"""
import os
import django
from django.conf import settings
from django.urls import reverse, NoReverseMatch

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

def find_admin_url():
    """Find the correct admin URL"""
    print("🔍 Finding Admin URL Configuration")
    print("=" * 35)
    
    # Get the admin URL from settings
    admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    print(f"Configured Admin URL: {admin_url}")
    
    # Try to resolve the admin URL
    try:
        admin_index_url = reverse('admin:index')
        print(f"Resolved Admin Index URL: {admin_index_url}")
    except NoReverseMatch:
        print("❌ Could not resolve admin:index URL pattern")
    
    # Show possible URLs to try
    print(f"\n🔧 Try accessing your admin panel at one of these URLs:")
    print(f"1. https://christopher-erick-otieno-portfolio.onrender.com/{admin_url}")
    print(f"2. https://christopher-erick-otieno-portfolio.onrender.com/admin/")
    print(f"3. https://christopher-erick-otieno-portfolio.onrender.com/secure-admin-ceo789/")
    print(f"4. https://christopher-erick-otieno-portfolio.onrender.com/secure-admin-path-12345/")
    
    # Show environment variables
    print(f"\n📋 Current Environment Variables:")
    env_vars = ['ADMIN_URL', 'SECRET_KEY', 'DEBUG']
    for var in env_vars:
        value = os.getenv(var, 'Not set')
        # Mask sensitive values
        if var == 'SECRET_KEY' and value != 'Not set':
            value = f"{value[:5]}...{value[-5:]}" if len(value) > 10 else "********"
        print(f"  {var}: {value}")

if __name__ == '__main__':
    find_admin_url()