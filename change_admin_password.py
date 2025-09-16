#!/usr/bin/env python
"""
Script to securely change the Django admin password
"""

import os
import django
import getpass
from config import AdminConfig

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def change_admin_password():
    """Change the admin user password securely"""
    try:
        admin_user = User.objects.get(username=AdminConfig.get_admin_username())
        
        print("🔐 Changing admin password for cybersecurity portfolio")
        print(f"Username: {AdminConfig.get_admin_username()}")
        print(f"Email: {AdminConfig.get_admin_email()}")
        print()
        
        # Get new password securely (won't show on screen)
        new_password = getpass.getpass("Enter new secure password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("❌ Passwords don't match. Please try again.")
            return False
            
        if len(new_password) < 8:
            print("❌ Password must be at least 8 characters long.")
            return False
            
        # Update password
        admin_user.set_password(new_password)
        admin_user.save()
        
        print("✅ Admin password updated successfully!")
        print(f"🌐 You can now login at: http://127.0.0.1:8000/admin/")
        print(f"👤 Username: {AdminConfig.get_admin_username()}")
        print("🔑 Use your new password")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Admin user not found. Please run create_admin.py first.")
        return False
    except Exception as e:
        print(f"❌ Error changing password: {e}")
        return False

if __name__ == '__main__':
    change_admin_password()