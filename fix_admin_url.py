#!/usr/bin/env python
"""
Fix script for admin URL issues in deployed application
"""
import os
import django
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

User = get_user_model()

def check_and_fix_admin_url():
    """Check and fix admin URL issues"""
    print("🔧 Admin URL Fix Script")
    print("=" * 25)
    
    # 1. Check current admin URL configuration
    from django.conf import settings
    current_admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
    print(f"Current ADMIN_URL setting: {current_admin_url}")
    
    # 2. Check environment variable
    env_admin_url = os.getenv('ADMIN_URL', 'Not set')
    print(f"Environment variable ADMIN_URL: {env_admin_url}")
    
    # 3. If they don't match, there might be a deployment issue
    if env_admin_url != current_admin_url and env_admin_url != 'Not set':
        print("⚠️  Environment variable and Django settings don't match!")
        print("   This suggests the environment variables may not have been applied correctly.")
        print("   Try redeploying your application.")
    
    # 4. Check if admin user exists
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    try:
        admin_user = User.objects.get(username=admin_username)
        print(f"✅ Admin user '{admin_username}' exists")
    except User.DoesNotExist:
        print(f"❌ Admin user '{admin_username}' does not exist")
        print("   You may need to create a superuser.")
    
    # 5. Provide instructions
    print(f"\n📋 Instructions to fix the admin URL issue:")
    print(f"1. Go to your Render dashboard")
    print(f"2. Select your web service: 'christopher-erick-otieno-portfolio'")
    print(f"3. Go to 'Environment Variables' section")
    print(f"4. Verify that ADMIN_URL is set to 'secure-admin-path-12345/'")
    print(f"5. If it's not set correctly, update it")
    print(f"6. Click 'Save Changes'")
    print(f"7. Redeploy your application by clicking 'Manual Deploy' -> 'Deploy latest commit'")
    print(f"8. Wait for deployment to complete (5-10 minutes)")
    
    print(f"\n🔓 Alternative Access:")
    print(f"If the above doesn't work, try accessing the admin panel at:")
    print(f"https://christopher-erick-otieno-portfolio.onrender.com/secure-admin-ceo789/")
    print(f"(This is the default admin URL that seems to be working)")
    
    print(f"\n🔐 To create a superuser if needed:")
    print(f"1. In Render dashboard, go to your web service")
    print(f"2. Click on 'Shell' tab")
    print(f"3. Run: python manage.py createsuperuser")
    print(f"4. Follow the prompts to create an admin user")

if __name__ == '__main__':
    check_and_fix_admin_url()