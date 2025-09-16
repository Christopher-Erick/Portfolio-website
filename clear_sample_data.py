#!/usr/bin/env python
"""
Script to clear sample projects and prepare for real cybersecurity portfolio data
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from portfolio.models import Category, Technology, Project, ProjectFeature, ProjectImage


def clear_sample_projects():
    """Remove sample projects but keep categories and technologies"""
    print("Clearing sample projects...")
    
    # Delete all projects and their related data
    ProjectImage.objects.all().delete()
    ProjectFeature.objects.all().delete()
    Project.objects.all().delete()
    
    print(f"Cleared all sample projects")
    print(f"Remaining categories: {Category.objects.count()}")
    print(f"Remaining technologies: {Technology.objects.count()}")


def add_more_technologies():
    """Add additional cybersecurity technologies that might be needed"""
    additional_techs = [
        {'name': 'Nikto', 'icon': 'fas fa-spider', 'color': '#FF4444'},
        {'name': 'Hashcat', 'icon': 'fas fa-key', 'color': '#FFA500'},
        {'name': 'John the Ripper', 'icon': 'fas fa-unlock', 'color': '#8B4513'},
        {'name': 'Aircrack-ng', 'icon': 'fas fa-wifi', 'color': '#0066CC'},
        {'name': 'Sqlmap', 'icon': 'fas fa-database', 'color': '#DC143C'},
        {'name': 'OpenVAS', 'icon': 'fas fa-search', 'color': '#228B22'},
        {'name': 'Volatility', 'icon': 'fas fa-memory', 'color': '#4B0082'},
        {'name': 'YARA', 'icon': 'fas fa-fingerprint', 'color': '#800080'},
        {'name': 'Snort', 'icon': 'fas fa-shield-alt', 'color': '#FF6347'},
        {'name': 'pfSense', 'icon': 'fas fa-fire', 'color': '#1E90FF'},
        {'name': 'Docker', 'icon': 'fab fa-docker', 'color': '#2496ED'},
        {'name': 'VirtualBox', 'icon': 'fas fa-cube', 'color': '#183A61'},
        {'name': 'VMware', 'icon': 'fas fa-server', 'color': '#607078'},
        {'name': 'Windows Server', 'icon': 'fab fa-windows', 'color': '#0078D4'},
        {'name': 'Active Directory', 'icon': 'fas fa-users-cog', 'color': '#0078D4'},
    ]
    
    for tech_data in additional_techs:
        technology, created = Technology.objects.get_or_create(
            name=tech_data['name'],
            defaults=tech_data
        )
        if created:
            print(f"Added technology: {technology.name}")


def main():
    print("Preparing portfolio system for real projects...")
    
    # Clear sample projects
    clear_sample_projects()
    
    # Add more technologies that might be useful
    print("\nAdding additional cybersecurity technologies...")
    add_more_technologies()
    
    print(f"\nSystem ready for real projects!")
    print(f"Available categories: {Category.objects.count()}")
    print(f"Available technologies: {Technology.objects.count()}")
    
    print("\nCategories available:")
    for cat in Category.objects.all():
        print(f"  - {cat.name} ({cat.slug})")
    
    print(f"\nTotal technologies available: {Technology.objects.count()}")


if __name__ == '__main__':
    main()