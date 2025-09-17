#!/usr/bin/env python
"""
Script to generate Render environment variables for proper deployment
This script outputs the environment variables that should be set in Render dashboard
"""

def print_render_env_vars():
    """Print environment variables needed for Render deployment"""
    env_vars = {
        "SECRET_KEY": "your-very-secure-secret-key-here",
        "DEBUG": "False",
        "DATABASE_URL": "your-railway-postgresql-database-url",
        "ALLOWED_HOSTS": "christopher-erick-otieno-portfolio.onrender.com,render.app",
        "RENDER_EXTERNAL_HOSTNAME": "christopher-erick-otieno-portfolio.onrender.com",
        "FULL_NAME": "Christopher Erick Otieno",
        "EMAIL": "erikchris54@gmail.com",
        "GITHUB_USERNAME": "Christopher-Erick",
        "TRYHACKME_USERNAME": "erikchris54",
        "HACKTHEBOX_USERNAME": "ChristopherErick",
        "TAGLINE": "Building secure digital ecosystems from the ground up — where cybersecurity meets seamless operations, data drives decisions, and complex challenges become elegant solutions.",
        "PHONE": "+254758081580",
        "LOCATION": "Nairobi, Kenya",
        "ADMIN_USERNAME": "portfolio_admin_x7k9",
        "ADMIN_EMAIL": "erikchris54@gmail.com",
        "ADMIN_URL": "secure-admin-path-12345/",
        "CONTACT_EMAIL": "erikchris54@gmail.com",
        "SECURE_SSL_REDIRECT": "True",
        "SESSION_COOKIE_SECURE": "True",
        "CSRF_COOKIE_SECURE": "True"
    }
    
    print("📝 Environment variables for Render deployment:")
    print("=" * 50)
    
    for key, value in env_vars.items():
        print(f"{key}={value}")
    
    print("\n📋 Instructions:")
    print("1. Go to your Render dashboard")
    print("2. Select your web service")
    print("3. Go to 'Environment Variables' section")
    print("4. Add each of the variables above")
    print("5. For SECRET_KEY, generate a secure random key")
    print("6. For DATABASE_URL, use your Railway PostgreSQL URL")
    print("7. Redeploy your application")


if __name__ == '__main__':
    print_render_env_vars()