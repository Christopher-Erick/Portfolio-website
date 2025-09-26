#!/usr/bin/env python
"""
Script to help set up production environment variables
"""
import os
import sys
from pathlib import Path

def generate_render_env_file():
    """Generate environment variables for Render deployment"""
    env_vars = {
        # Django Configuration
        "DEBUG": "False",
        "SECRET_KEY": "your-super-secret-key-here-generate-a-new-one",
        "ALLOWED_HOSTS": "yourdomain.com,www.yourdomain.com,your-app-name.onrender.com",
        "ADMIN_URL": "secure-admin-path-12345/",
        
        # Database Configuration
        "DATABASE_URL": "postgres://username:password@host:port/database_name",
        
        # Email Configuration
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": "587",
        "EMAIL_USE_TLS": "True",
        "EMAIL_HOST_USER": "your-email@gmail.com",
        "EMAIL_HOST_PASSWORD": "your-app-specific-password",
        "DEFAULT_FROM_EMAIL": "your-email@gmail.com",
        "CONTACT_EMAIL": "your-email@gmail.com",
        
        # Cloudinary Configuration
        "CLOUDINARY_CLOUD_NAME": "dge5xurfz",
        "CLOUDINARY_API_KEY": "172734151545842",
        "CLOUDINARY_API_SECRET": "Yry1SKCjiA8ddXCP8lqclK-B9u4",
        
        # Personal Information
        "FULL_NAME": "Christopher Erick Otieno",
        "EMAIL": "erikchris54@gmail.com",
        "GITHUB_USERNAME": "Christopher-Erick",
        "TRYHACKME_USERNAME": "erikchris54",
        "HACKTHEBOX_USERNAME": "ChristopherErick",
        "TAGLINE": "Building secure digital ecosystems from the ground up — where cybersecurity meets seamless operations, data drives decisions, and complex challenges become elegant solutions.",
        "PHONE": "+254758081580",
        "LOCATION": "Nairobi, Kenya",
        
        # Admin Configuration
        "ADMIN_USERNAME": "portfolio_admin_x7k9",
        "ADMIN_EMAIL": "erikchris54@gmail.com",
        
        # Security Settings
        "SECURE_SSL_REDIRECT": "True",
        "SESSION_COOKIE_SECURE": "True",
        "CSRF_COOKIE_SECURE": "True",
    }
    
    # Write to render.env file
    with open("render.env", "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("Render environment file (render.env) created successfully!")
    print("Remember to update the placeholder values with your actual values.")

def generate_fly_env_file():
    """Generate environment variables for Fly.io deployment"""
    env_vars = {
        # Django Configuration
        "DEBUG": "False",
        "SECRET_KEY": "your-super-secret-key-here-generate-a-new-one",
        "ALLOWED_HOSTS": "yourdomain.com,www.yourdomain.com,your-app-name.fly.dev",
        "ADMIN_URL": "secure-admin-path-12345/",
        
        # Database Configuration
        "DATABASE_URL": "postgres://username:password@host:port/database_name",
        
        # Email Configuration
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": "587",
        "EMAIL_USE_TLS": "True",
        "EMAIL_HOST_USER": "your-email@gmail.com",
        "EMAIL_HOST_PASSWORD": "your-app-specific-password",
        "DEFAULT_FROM_EMAIL": "your-email@gmail.com",
        "CONTACT_EMAIL": "your-email@gmail.com",
        
        # Cloudinary Configuration
        "CLOUDINARY_CLOUD_NAME": "dge5xurfz",
        "CLOUDINARY_API_KEY": "172734151545842",
        "CLOUDINARY_API_SECRET": "Yry1SKCjiA8ddXCP8lqclK-B9u4",
        
        # Personal Information
        "FULL_NAME": "Christopher Erick Otieno",
        "EMAIL": "erikchris54@gmail.com",
        "GITHUB_USERNAME": "Christopher-Erick",
        "TRYHACKME_USERNAME": "erikchris54",
        "HACKTHEBOX_USERNAME": "ChristopherErick",
        "TAGLINE": "Building secure digital ecosystems from the ground up — where cybersecurity meets seamless operations, data drives decisions, and complex challenges become elegant solutions.",
        "PHONE": "+254758081580",
        "LOCATION": "Nairobi, Kenya",
        
        # Admin Configuration
        "ADMIN_USERNAME": "portfolio_admin_x7k9",
        "ADMIN_EMAIL": "erikchris54@gmail.com",
        
        # Security Settings
        "SECURE_SSL_REDIRECT": "True",
        "SESSION_COOKIE_SECURE": "True",
        "CSRF_COOKIE_SECURE": "True",
    }
    
    # Write to fly.env file
    with open("fly.env", "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("Fly.io environment file (fly.env) created successfully!")
    print("Remember to update the placeholder values with your actual values.")

def main():
    print("Production Environment Setup Script")
    print("=" * 40)
    
    print("\n1. Render Deployment")
    print("2. Fly.io Deployment")
    print("3. Both")
    
    choice = input("\nSelect deployment platform (1-3): ").strip()
    
    if choice == "1":
        generate_render_env_file()
    elif choice == "2":
        generate_fly_env_file()
    elif choice == "3":
        generate_render_env_file()
        generate_fly_env_file()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()