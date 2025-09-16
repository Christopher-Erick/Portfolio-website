#!/usr/bin/env python3
"""
Production Environment Setup Script
This script helps set up a production-ready environment for the portfolio website.
"""

import os
import secrets
import string
import sys
from pathlib import Path

def generate_secret_key(length=50):
    """Generate a secure Django secret key."""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Remove characters that might cause issues in environment variables
    chars = chars.replace('"', '').replace("'", '').replace('\\', '').replace('`', '')
    return ''.join(secrets.choice(chars) for _ in range(length))

def setup_production_env():
    """Set up production environment variables."""
    print("Setting up production environment...")
    
    # Check if .env.production exists
    env_file = Path('.env.production')
    if not env_file.exists():
        print("Error: .env.production file not found!")
        return False
    
    # Read the current .env.production file
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    # Replace placeholders with actual values
    # Note: In a real production setup, you would prompt for these values
    # For this script, we'll show what needs to be updated
    
    print("\n=== Production Environment Setup ===")
    print("The following values need to be configured in your .env.production file:")
    print("")
    print("1. SECRET_KEY:")
    print(f"   {secret_key}")
    print("")
    print("2. POSTGRES_PASSWORD:")
    print("   Set a secure password for your PostgreSQL database")
    print("")
    print("3. ALLOWED_HOSTS:")
    print("   Set your actual domain (e.g., yourdomain.com,www.yourdomain.com)")
    print("")
    print("4. Email Configuration:")
    print("   - EMAIL_HOST: Your SMTP server")
    print("   - EMAIL_HOST_USER: Your email address")
    print("   - EMAIL_HOST_PASSWORD: Your app-specific password")
    print("   - CONTACT_EMAIL: Your contact email")
    print("")
    print("After updating these values, copy .env.production to .env:")
    print("cp .env.production .env")
    print("")
    
    # Save the generated secret key to a file for easy access
    with open('.secret_key', 'w') as f:
        f.write(secret_key)
    
    print("A secret key has been generated and saved to .secret_key")
    print("Please update your .env.production file with this key and other required values.")
    
    return True

def check_production_readiness():
    """Check if the application is ready for production."""
    print("Checking production readiness...")
    
    # Check if required files exist
    required_files = [
        'Dockerfile',
        'docker-compose.yml',
        'config/nginx/nginx.conf',
        '.env.production'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # Check if config/certs directory exists
    if not Path('config/certs').exists():
        print("⚠️  Warning: config/certs directory not found")
        print("   You need to set up SSL certificates for production")
    
    # Check if .env.production has been updated
    env_file = Path('.env.production')
    with open(env_file, 'r') as f:
        content = f.read()
    
    placeholders = [
        'your-super-secret-key-here',
        'your-secure-database-password-here',
        'yourdomain.com',
        'your-email@gmail.com',
        'your-app-specific-password'
    ]
    
    unfilled_placeholders = []
    for placeholder in placeholders:
        if placeholder in content:
            unfilled_placeholders.append(placeholder)
    
    if unfilled_placeholders:
        print("⚠️  Warning: The following placeholders still need to be filled in .env.production:")
        for placeholder in unfilled_placeholders:
            print(f"   - {placeholder}")
        return False
    
    print("✅ All required files are present")
    print("✅ Basic production setup appears to be complete")
    print("")
    print("Next steps:")
    print("1. Generate SSL certificates")
    print("2. Copy .env.production to .env")
    print("3. Run: docker-compose up --build")
    print("4. Run initial setup commands")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_production_readiness()
    else:
        setup_production_env()