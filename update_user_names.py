#!/usr/bin/env python
"""
Script to update User model with correct first_name and last_name
"""

import os
import django
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

User = get_user_model()

def update_user_names():
    """Update all users with correct first_name and last_name"""
    # Update all users to have proper first_name and last_name
    users = User.objects.all()
    
    for user in users:
        if user.first_name == '' and user.last_name == '':
            # Split the full name from the environment variable
            full_name = os.getenv('FULL_NAME', 'Christopher Erick Otieno')
            name_parts = full_name.split(' ', 1)
            
            if len(name_parts) == 2:
                first_name = name_parts[0]
                last_name = name_parts[1]
            else:
                first_name = full_name
                last_name = ''
                
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(f"Updated user {user.username} with name: {first_name} {last_name}")
        else:
            print(f"User {user.username} already has name data: {user.first_name} {user.last_name}")

if __name__ == '__main__':
    update_user_names()