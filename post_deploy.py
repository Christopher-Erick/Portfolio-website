#!/usr/bin/env python
"""
Post-deployment script to populate database with initial data
This script should be run after deployment to ensure the database has all necessary data
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.core.management import execute_from_command_line
from populate_all_data import main as populate_data


def run_post_deploy():
    """Run post-deployment tasks"""
    print("🚀 Running post-deployment tasks...")
    
    try:
        # Run migrations to ensure database schema is up to date
        print("🔧 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Populate data
        print("📊 Populating database with initial data...")
        populate_data()
        
        print("✅ Post-deployment tasks completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during post-deployment: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_post_deploy()