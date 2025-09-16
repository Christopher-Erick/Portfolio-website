"""
Signal handlers for security events
"""
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
import logging

logger = logging.getLogger('django.security')


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """Log failed login attempts"""
    if not request:
        return
    
    # Get client IP
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    client_ip = get_client_ip(request)
    username = credentials.get('username', 'unknown')
    
    # Log the event
    try:
        from .models import SecurityEvent
        SecurityEvent.log_event(
            event_type='login_failed',
            ip_address=client_ip,
            description=f'Failed login attempt for username: {username}',
            severity='medium',
            username=username,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path,
            method=request.method
        )
        logger.warning(f'Failed login attempt - IP: {client_ip}, Username: {username}')
    except Exception as e:
        logger.error(f'Failed to log failed login event: {e}')


@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    """Log successful login attempts"""
    if not request:
        return
    
    # Get client IP
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    client_ip = get_client_ip(request)
    
    # Log the event
    try:
        from .models import SecurityEvent
        SecurityEvent.log_event(
            event_type='login_success',
            ip_address=client_ip,
            description=f'Successful login for user: {user.username}',
            severity='low',
            username=user.username,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path,
            method=request.method
        )
        logger.info(f'Successful login - IP: {client_ip}, User: {user.username}')
    except Exception as e:
        logger.error(f'Failed to log successful login event: {e}')