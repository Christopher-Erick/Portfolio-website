#!/usr/bin/env python
"""
Script to create Django admin superuser for production deployment
"""
import os
import django
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

User = get_user_model()

def create_admin_user():
    """Create admin user with environment variables"""
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    # For production, you should set this securely
    password = os.getenv('ADMIN_PASSWORD')
    
    if not password:
        print("❌ ADMIN_PASSWORD environment variable not set")
        print("Please set ADMIN_PASSWORD in your environment variables")
        return
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"📧 Email: {email}")
        print("🔑 Password: [Set from ADMIN_PASSWORD environment variable]")
    else:
        print(f"ℹ️ Superuser '{username}' already exists.")
        # Update the password if needed
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ Superuser '{username}' password updated.")

if __name__ == '__main__':
    create_admin_user()