#!/usr/bin/env python3
"""
Production Setup Verification Script
This script verifies that all components are properly configured for production deployment.
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files and directories exist."""
    print("Checking file structure...")
    
    required_paths = [
        'Dockerfile',
        'docker-compose.yml',
        'requirements.txt',
        'manage.py',
        'config/nginx/nginx.conf',
        'config/certs',
        '.env.production',
        '.env.development'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
    
    if missing_paths:
        print("❌ Missing required paths:")
        for path in missing_paths:
            print(f"   - {path}")
        return False
    
    print("✅ All required files and directories are present")
    return True

def check_docker_compose():
    """Check Docker Compose configuration."""
    print("Checking Docker Compose configuration...")
    
    try:
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
        
        required_sections = [
            'services:',
            'web:',
            'db:',
            'nginx:',
            'volumes:',
            'networks:'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print("❌ Missing sections in docker-compose.yml:")
            for section in missing_sections:
                print(f"   - {section}")
            return False
        
        print("✅ Docker Compose configuration is complete")
        return True
    except Exception as e:
        print(f"❌ Error reading docker-compose.yml: {e}")
        return False

def check_nginx_config():
    """Check Nginx configuration."""
    print("Checking Nginx configuration...")
    
    try:
        with open('config/nginx/nginx.conf', 'r') as f:
            content = f.read()
        
        required_sections = [
            'upstream django',
            'server {',
            'listen 80',
            'listen 443 ssl',
            'proxy_pass http://django'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print("❌ Missing sections in nginx.conf:")
            for section in missing_sections:
                print(f"   - {section}")
            return False
        
        print("✅ Nginx configuration is complete")
        return True
    except Exception as e:
        print(f"❌ Error reading nginx.conf: {e}")
        return False

def check_environment_templates():
    """Check environment template files."""
    print("Checking environment templates...")
    
    try:
        # Check development template
        with open('.env.development', 'r') as f:
            dev_content = f.read()
        
        # Check production template
        with open('.env.production', 'r') as f:
            prod_content = f.read()
        
        # Verify personal information is preserved
        personal_info = [
            'Christopher Erick Otieno',
            'erikchris54@gmail.com',
            '+254758081580',
            'Nairobi, Kenya',
            'Christopher-Erick',
            'erikchris54',
            'ChristopherErick'
        ]
        
        missing_info = []
        for info in personal_info:
            if info not in prod_content:
                missing_info.append(info)
        
        if missing_info:
            print("❌ Missing personal information in .env.production:")
            for info in missing_info:
                print(f"   - {info}")
            return False
        
        print("✅ Personal information is preserved in environment templates")
        return True
    except Exception as e:
        print(f"❌ Error checking environment templates: {e}")
        return False

def check_requirements():
    """Check Python requirements."""
    print("Checking Python requirements...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'Django',
            'Pillow',
            'reportlab',
            'whitenoise',
            'gunicorn',
            'psycopg2-binary'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print("❌ Missing packages in requirements.txt:")
            for package in missing_packages:
                print(f"   - {package}")
            return False
        
        print("✅ All required Python packages are listed")
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def main():
    """Main verification function."""
    print("=== Production Setup Verification ===")
    print("")
    
    checks = [
        check_file_structure,
        check_docker_compose,
        check_nginx_config,
        check_environment_templates,
        check_requirements
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print("")
    
    if all_passed:
        print("🎉 All checks passed! Your application is ready for production setup.")
        print("")
        print("Next steps:")
        print("1. Generate a secure secret key: python setup_production.py")
        print("2. Update .env.production with your actual values")
        print("3. Copy .env.production to .env: cp .env.production .env")
        print("4. Generate SSL certificates")
        print("5. Run: docker-compose up --build")
        print("6. Run initial setup commands")
        print("7. Test all functionality")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("See PRODUCTION_CHECKLIST.md for detailed instructions.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())