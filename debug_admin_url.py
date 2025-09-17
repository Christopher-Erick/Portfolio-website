#!/usr/bin/env python
"""
Debug script to check admin URL configuration
"""
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

def debug_admin_url():
    """Debug admin URL configuration"""
    print("🔍 Debugging Admin URL Configuration")
    print("=" * 40)
    
    # Check environment variable
    env_admin_url = os.getenv('ADMIN_URL')
    print(f"Environment Variable ADMIN_URL: {env_admin_url}")
    
    # Check Django settings
    django_admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    print(f"Django Settings ADMIN_URL: {django_admin_url}")
    
    # Check if they match
    if env_admin_url == django_admin_url:
        print("✅ Environment variable and Django settings match")
    else:
        print("❌ Environment variable and Django settings do NOT match")
    
    print(f"\n🔧 To access your admin panel, go to:")
    print(f"   https://christopher-erick-otieno-portfolio.onrender.com/{django_admin_url}")
    
    # Also check if the default is being used
    if django_admin_url == 'secure-admin-ceo789/':
        print("\n⚠️  Note: The default admin URL 'secure-admin-ceo789/' is being used")
        print("   If you set a different URL in Render, it might not be taking effect")
    
    print(f"\n📋 To fix this issue:")
    print(f"1. Go to your Render dashboard")
    print(f"2. Select your web service")
    print(f"3. Go to 'Environment Variables' section")
    print(f"4. Make sure ADMIN_URL is set to the value you want")
    print(f"5. Redeploy your application")

if __name__ == '__main__':
    debug_admin_url()