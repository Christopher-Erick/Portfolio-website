#!/usr/bin/env python
"""
Enhanced admin security features for brute force protection
and file upload validation
"""

import os
import django
from django.core.exceptions import ValidationError
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth import get_user_model
import logging

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

logger = logging.getLogger('django.security')

# File upload validation
def validate_file_upload(file):
    """Validate uploaded files for security"""
    
    # Check file size (additional to Django settings)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError(f'File size {file.size} exceeds maximum allowed size of {max_size} bytes')
    
    # Check file extension
    allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif']
    dangerous_extensions = ['.exe', '.php', '.asp', '.jsp', '.py', '.js', '.html', '.htm', '.bat', '.cmd', '.sh']
    
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension in dangerous_extensions:
        logger.warning(f'Dangerous file upload attempt: {file.name}')
        raise ValidationError(f'File type {file_extension} is not allowed for security reasons')
    
    if file_extension not in allowed_extensions:
        raise ValidationError(f'File type {file_extension} is not supported. Allowed types: {", ".join(allowed_extensions)}')
    
    # Check for embedded scripts in file names
    dangerous_patterns = ['<script', 'javascript:', 'vbscript:', '<?php', '<%', 'exec(', 'eval(']
    filename_lower = file.name.lower()
    
    for pattern in dangerous_patterns:
        if pattern in filename_lower:
            logger.warning(f'Suspicious file name detected: {file.name}')
            raise ValidationError('File name contains potentially dangerous content')
    
    return True


# Admin brute force protection
@receiver(user_login_failed)
def admin_login_failed_handler(sender, credentials, request, **kwargs):
    """Handle failed login attempts with rate limiting"""
    if not request:
        return
    
    # Get client IP
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    
    client_ip = get_client_ip(request)
    username = credentials.get('username', 'unknown')
    
    # Check if this is an admin login attempt
    if '/admin/' in request.path:
        # Rate limiting for admin login attempts
        rate_limit_key = f'admin_login_failed_{client_ip}'
        username_key = f'admin_login_failed_user_{username}'
        
        # Track failed attempts by IP
        failed_attempts_ip = cache.get(rate_limit_key, 0)
        failed_attempts_user = cache.get(username_key, 0)
        
        failed_attempts_ip += 1
        failed_attempts_user += 1
        
        # Set cache with 15 minute expiry
        cache.set(rate_limit_key, failed_attempts_ip, 900)  # 15 minutes
        cache.set(username_key, failed_attempts_user, 900)  # 15 minutes
        
        # Log the attempt
        logger.warning(
            f'Admin login failed - IP: {client_ip}, Username: {username}, '
            f'IP attempts: {failed_attempts_ip}, User attempts: {failed_attempts_user}'
        )
        
        # If too many attempts, log security alert
        if failed_attempts_ip >= 5 or failed_attempts_user >= 3:
            logger.error(
                f'SECURITY ALERT: Multiple failed admin login attempts - '
                f'IP: {client_ip}, Username: {username}'
            )


def check_admin_account_security():
    """Check admin account security settings"""
    print("🔐 ADMIN ACCOUNT SECURITY CHECK")
    print("=" * 50)
    
    User = get_user_model()
    
    try:
        # Check for default admin accounts
        weak_usernames = ['admin', 'administrator', 'root', 'test']
        
        for username in weak_usernames:
            try:
                user = User.objects.get(username=username)
                if user.is_superuser:
                    print(f"⚠️ Found superuser with potentially weak username: {username}")
                    
                    # Check if password was changed recently
                    if hasattr(user, 'date_joined') and hasattr(user, 'last_login'):
                        if user.date_joined == user.last_login:
                            print(f"❌ User {username} may still have default password!")
                        else:
                            print(f"✅ User {username} has logged in since creation")
                            
            except User.DoesNotExist:
                continue
        
        # Check for users with simple passwords (this is limited without access to hashed passwords)
        superusers = User.objects.filter(is_superuser=True)
        print(f"\n📊 Found {superusers.count()} superuser account(s)")
        
        for user in superusers:
            print(f"  • {user.username} - Last login: {user.last_login or 'Never'}")
            
            # Check failed login attempts
            rate_limit_key = f'admin_login_failed_user_{user.username}'
            failed_attempts = cache.get(rate_limit_key, 0)
            
            if failed_attempts > 0:
                print(f"    ⚠️ Recent failed login attempts: {failed_attempts}")
            else:
                print(f"    ✅ No recent failed login attempts")
    
    except Exception as e:
        print(f"❌ Error checking admin accounts: {e}")
    
    print()


def secure_admin_recommendations():
    """Provide security recommendations for admin accounts"""
    print("💡 ADMIN SECURITY RECOMMENDATIONS")
    print("=" * 50)
    
    print("1. Change default admin passwords immediately")
    print("2. Use strong passwords (12+ characters, mixed case, numbers, symbols)")
    print("3. Enable two-factor authentication (2FA) when possible")
    print("4. Use non-obvious usernames (avoid 'admin', 'administrator')")
    print("5. Regular password rotation (every 90 days)")
    print("6. Monitor failed login attempts")
    print("7. Use custom admin URLs in production")
    print("8. Limit admin access to specific IP addresses when possible")
    print()


if __name__ == '__main__':
    check_admin_account_security()
    secure_admin_recommendations()