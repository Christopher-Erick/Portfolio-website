#!/usr/bin/env python
"""
Script to create Django admin superuser for portfolio upload access
"""

import os
import django
from django.contrib.auth import get_user_model
from config import AdminConfig

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

User = get_user_model()

# Create superuser if doesn't exist
username = AdminConfig.get_admin_username()
email = AdminConfig.get_admin_email()
password = input('Enter admin password: ')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"📧 Email: {email}")
    print(f"🔑 Password: [Hidden for security]")
    print("\n🌐 Admin URL: http://127.0.0.1:8000/admin/")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")

print("\n📝 Instructions to upload your files:")
print("1. Start the Django server: python manage.py runserver")
print("2. Open http://127.0.0.1:8000/admin/")
print("3. Login with the credentials above")
print("4. Click on 'Projects' under PORTFOLIO section")
print("5. Find your 'Security Assessment Methodology Study' project")
print("6. Click on it to edit")
print("7. Upload your image in 'Featured image' field")
print("8. Upload your writeup document in 'Writeup document' field")
print("9. Save the project")