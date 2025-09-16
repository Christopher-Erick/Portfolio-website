"""
Security middleware for enhanced protection
"""
import logging
from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re

logger = logging.getLogger('django.security')


class HttpResponseTooManyRequests(HttpResponse):
    """Custom 429 Too Many Requests response"""
    status_code = 429


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add additional security headers to responses"""
    
    def process_response(self, request, response):
        # Content Security Policy
        if not settings.DEBUG:
            csp_header = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://kit.fontawesome.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
                "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
            response['Content-Security-Policy'] = csp_header
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """Rate limiting middleware to prevent abuse"""
    
    def process_request(self, request):
        # Skip rate limiting for static files and admin in development
        if settings.DEBUG and (
            request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path.startswith('/' + getattr(settings, 'ADMIN_URL', 'admin/'))
        ):
            return None
        
        # Skip rate limiting for GET requests to main pages in development
        if settings.DEBUG and request.method == 'GET' and request.path in ['/', '/home/', '/portfolio/', '/blog/', '/resume/', '/contact/']:
            return None
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Different rate limits for different endpoints
        if request.path == '/contact/' and request.method == 'POST':
            # Contact form: 10 requests per 15 minutes (increased from 5)
            rate_limit_key = f'rate_limit_contact_{client_ip}'
            max_requests = 10
            time_window = 900  # 15 minutes
        elif request.path.startswith('/' + getattr(settings, 'ADMIN_URL', 'admin/')):
            # Admin panel: 50 requests per 5 minutes (increased from 20)
            rate_limit_key = f'rate_limit_admin_{client_ip}'
            max_requests = 50
            time_window = 300  # 5 minutes
        else:
            # General pages: 200 requests per 5 minutes (increased from 100)
            rate_limit_key = f'rate_limit_general_{client_ip}'
            max_requests = 200
            time_window = 300  # 5 minutes
        
        # Check rate limit
        current_requests = cache.get(rate_limit_key, 0)
        
        if current_requests >= max_requests:
            logger.warning(f'Rate limit exceeded for IP {client_ip} on {request.path}')
            # Log rate limit violation
            try:
                from .models import SecurityEvent
                SecurityEvent.log_event(
                    event_type='rate_limit',
                    ip_address=client_ip,
                    description=f'Rate limit exceeded on {request.path} ({current_requests}/{max_requests} requests)',
                    severity='medium',
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    path=request.path,
                    method=request.method
                )
            except Exception as e:
                logger.error(f'Failed to log rate limit event: {e}')
            return HttpResponseTooManyRequests('Rate limit exceeded. Please try again later.')
        
        # Increment counter
        cache.set(rate_limit_key, current_requests + 1, time_window)
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address, considering proxy headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityLoggingMiddleware(MiddlewareMixin):
    """Log security-related events"""
    
    def process_request(self, request):
        # Log suspicious requests
        suspicious_patterns = [
            r'\.\./',  # Directory traversal
            r'<script',  # XSS attempts
            r'union\s+select',  # SQL injection
            r'exec\(',  # Code execution
            r'eval\(',  # Code evaluation
            r'base64_decode',  # Encoded payloads
        ]
        
        # Check URL and parameters for suspicious patterns
        full_url = request.get_full_path()
        for pattern in suspicious_patterns:
            if re.search(pattern, full_url, re.IGNORECASE):
                client_ip = self.get_client_ip(request)
                logger.warning(
                    f'Suspicious request detected from IP {client_ip}: {full_url}'
                )
                # Log to database
                try:
                    from .models import SecurityEvent
                    SecurityEvent.log_event(
                        event_type='suspicious_request',
                        ip_address=client_ip,
                        description=f'Suspicious pattern detected: {pattern}',
                        severity='medium',
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        path=request.path,
                        method=request.method
                    )
                except Exception as e:
                    logger.error(f'Failed to log security event: {e}')
                break
        
        # Log admin access attempts
        admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
        if request.path.startswith('/' + admin_url):
            client_ip = self.get_client_ip(request)
            logger.info(f'Admin access attempt from IP {client_ip}: {request.path}')
            # Log admin access
            try:
                from .models import SecurityEvent
                SecurityEvent.log_event(
                    event_type='admin_access',
                    ip_address=client_ip,
                    description=f'Admin panel access: {request.path}',
                    severity='low',
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    path=request.path,
                    method=request.method
                )
            except Exception as e:
                logger.error(f'Failed to log admin access event: {e}')
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address, considering proxy headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlockSuspiciousRequestsMiddleware(MiddlewareMixin):
    """Block obviously malicious requests"""
    
    def process_request(self, request):
        # Skip blocking in debug mode for normal browser requests
        if settings.DEBUG and request.method == 'GET':
            return None
            
        # Block requests with malicious user agents
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        malicious_agents = [
            'sqlmap', 'nikto', 'nessus', 'burp', 'dirbuster', 
            'gobuster', 'dirb', 'w3af', 'metasploit', 'masscan',
            'nmap', 'zap', 'acunetix', 'qualys'
        ]
        
        for agent in malicious_agents:
            if agent in user_agent:
                client_ip = self.get_client_ip(request)
                logger.warning(f'Malicious user agent detected from IP {client_ip}: {user_agent}')
                # Log malicious user agent
                try:
                    from .models import SecurityEvent
                    SecurityEvent.log_event(
                        event_type='security_scan',
                        ip_address=client_ip,
                        description=f'Malicious user agent detected: {agent}',
                        severity='high',
                        user_agent=user_agent,
                        path=request.path,
                        method=request.method
                    )
                except Exception as e:
                    logger.error(f'Failed to log malicious user agent event: {e}')
                return HttpResponseForbidden('Access denied - Malicious user agent detected')
        
        # Block requests with suspicious file extensions (only for direct file access)
        suspicious_extensions = ['.php', '.asp', '.jsp', '.cgi', '.pl']
        path = request.path.lower()
        
        for ext in suspicious_extensions:
            if path.endswith(ext):
                client_ip = self.get_client_ip(request)
                logger.warning(f'Request for suspicious file from IP {client_ip}: {path}')
                return HttpResponseForbidden('Access denied - Suspicious file request')
        
        # Block obvious SQL injection attempts in URL
        sql_patterns = [
            r'union\s+select', r'drop\s+table', r'insert\s+into', 
            r'delete\s+from', r'update\s+.*set', r'\bor\s+1=1\b'
        ]
        
        full_path = request.get_full_path().lower()
        for pattern in sql_patterns:
            if re.search(pattern, full_path, re.IGNORECASE):
                client_ip = self.get_client_ip(request)
                logger.warning(f'SQL injection attempt detected from IP {client_ip}: {full_path}')
                return HttpResponseForbidden('Access denied - SQL injection attempt detected')
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address, considering proxy headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip