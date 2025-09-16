import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User  
from django.utils.html import escape
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django.http import HttpRequest
import json
import os
import re
from .models import UserProfile, Education, Certification, Achievement, Testimonial, ContactSubmission, SecurityEvent, Skill, Experience
from config import PersonalConfig


def test_download_security_report(request):
    """Test view to download security report without authentication"""
    import csv
    from django.http import HttpResponse
    from .models import SecurityEvent
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="security_report_test.csv"'
    
    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow([
        'Event Type', 
        'Username', 
        'IP Address', 
        'Login Status', 
        'Description', 
        'Timestamp', 
        'User Agent',
        'Path',
        'Method'
    ])
    
    # Get all security events, ordered by timestamp
    security_events = SecurityEvent.objects.all().order_by('-created_at')
    
    # Write data rows
    for event in security_events:
        login_status = 'Failed' if event.event_type == 'login_failed' else 'Success' if event.event_type == 'login_success' else 'N/A'
        writer.writerow([
            event.get_event_type_display(),
            event.username,
            event.ip_address,
            login_status,
            event.description,
            event.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            event.user_agent,
            event.path,
            event.method
        ])
    
    return response


def _home_view(request):
    """Home page view with featured portfolio projects and testimonials"""
    # Import portfolio models only when needed to avoid circular imports
    try:
        from portfolio.models import Project
        # Optimized query with better select_related and prefetch_related
        featured_projects = Project.objects.filter(is_featured=True).select_related('category').prefetch_related('technologies')[:3]
    except ImportError:
        featured_projects = []
    
    # Get active testimonials with related data
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_projects': featured_projects,
        'testimonials': testimonials,
    }
    return render(request, 'main/home.html', context)


# Apply cache decorator with error handling
home = vary_on_headers('User-Agent')(_home_view)
try:
    # Try to apply cache decorator
    home = cache_page(60 * 5)(home)  # Cache for 5 minutes (reduced from 15)
except Exception as e:
    # If cache is not available, use the view without caching
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Cache not available for home view: {e}")
    home = _home_view


@csrf_protect
@require_http_methods(["GET", "POST"])
def contact(request):
    """Secure contact page view with form handling and rate limiting"""
    if request.method == 'POST':
        # Rate limiting by IP address
        client_ip = get_client_ip(request)
        rate_limit_key = f'contact_form_rate_limit_{client_ip}'
        
        # Check if user has exceeded rate limit (max 3 submissions per hour)
        submission_count = cache.get(rate_limit_key, 0)
        if submission_count >= 3:
            logger.warning(f'Rate limit exceeded for IP: {client_ip}')
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'error': 'Too many submissions. Please try again later.'
                }, status=429)
            else:
                # Handle form submission (non-AJAX)
                return render(request, 'main/contact.html', {
                    'error_message': 'Too many submissions. Please try again later.'
                })
        
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    logger.warning(f'Invalid JSON data received from IP: {client_ip}')
                    return JsonResponse({
                        'success': False, 
                        'error': 'Invalid form data. Please try again.'
                    })
            else:
                # Handle form data
                data = {
                    'name': request.POST.get('name', ''),
                    'email': request.POST.get('email', ''),
                    'subject': request.POST.get('subject', ''),
                    'message': request.POST.get('message', '')
                }
            
            # Extract and validate input data
            name = validate_and_sanitize_input(data.get('name', ''), 'name')
            email = validate_and_sanitize_input(data.get('email', ''), 'email')
            subject = validate_and_sanitize_input(data.get('subject', ''), 'subject')
            message = validate_and_sanitize_input(data.get('message', ''), 'message')
            
            # Validate required fields
            if not all([name, email, subject, message]):
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False, 
                        'error': 'All fields are required and must contain valid content.'
                    })
                else:
                    return render(request, 'main/contact.html', {
                        'error_message': 'All fields are required and must contain valid content.'
                    })
            
            # Additional security checks
            if len(message) > 2000:
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False, 
                        'error': 'Message is too long. Please limit to 2000 characters.'
                    })
                else:
                    return render(request, 'main/contact.html', {
                        'error_message': 'Message is too long. Please limit to 2000 characters.'
                    })
            
            # Check for spam patterns
            if is_spam_content(name + ' ' + subject + ' ' + message):
                logger.warning(f'Potential spam detected from IP: {client_ip}')
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False, 
                        'error': 'Message appears to be spam. Please contact us directly.'
                    })
                else:
                    return render(request, 'main/contact.html', {
                        'error_message': 'Message appears to be spam. Please contact us directly.'
                    })
            
            # Save contact submission to database with additional security info
            contact_submission = ContactSubmission.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Log contact submission as security event
            try:
                SecurityEvent.log_event(
                    event_type='contact_submission',
                    ip_address=client_ip,
                    description=f'Contact form submission from {name} ({email})',
                    severity='low',
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    path=request.path,
                    method=request.method
                )
            except Exception as e:
                logger.error(f'Failed to log contact submission event: {e}')
            
            # Log successful submission
            logger.info(f'Contact form submitted successfully: {contact_submission.id} from {client_ip}')
            
            # Send email notification using environment variable
            try:
                recipient_email = os.getenv('CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)
                send_mail(
                    f'Portfolio Contact: {subject}',
                    f'From: {name} ({email})\n\nMessage:\n{message}\n\nSubmission ID: {contact_submission.id}',
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    fail_silently=False,
                )
                logger.info(f'Email notification sent for submission: {contact_submission.id}')
            except Exception as e:
                logger.error(f'Failed to send email for submission {contact_submission.id}: {str(e)}')
                # Don't fail the request if email fails
            
            # Update rate limiting counter
            cache.set(rate_limit_key, submission_count + 1, 3600)  # 1 hour
            
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': True, 
                    'message': 'Thank you for your message! I will get back to you soon.'
                })
            else:
                # Handle form submission (non-AJAX)
                return render(request, 'main/contact.html', {
                    'success_message': 'Thank you for your message! I will get back to you soon.'
                })
            
        except ValidationError as e:
            logger.warning(f'Validation error from IP {client_ip}: {str(e)}')
            error_message = str(e) if str(e) else 'Please check your input and try again.'
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'error': error_message
                })
            else:
                return render(request, 'main/contact.html', {
                    'error_message': error_message
                })
        except Exception as e:
            logger.error(f'Unexpected error in contact form from IP {client_ip}: {str(e)}')
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'error': 'Sorry, there was an error processing your request. Please try again later.'
                })
            else:
                return render(request, 'main/contact.html', {
                    'error_message': 'Sorry, there was an error processing your request. Please try again later.'
                })
    
    return render(request, 'main/contact.html')


def get_client_ip(request):
    """Get client IP address, considering proxy headers"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_and_sanitize_input(value, field_type):
    """Validate and sanitize input data"""
    if not value or not isinstance(value, str):
        return ''
    
    # Remove potentially dangerous characters
    value = escape(value.strip())
    
    if field_type == 'email':
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise ValidationError('Invalid email address')
    
    elif field_type == 'name':
        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-\']{2,50}$", value):
            raise ValidationError('Name contains invalid characters')
        return value
    
    elif field_type == 'subject':
        # Remove excessive whitespace and limit length
        value = re.sub(r'\s+', ' ', value)
        if len(value) > 200:
            raise ValidationError('Subject is too long')
        return value
    
    elif field_type == 'message':
        # Remove excessive whitespace
        value = re.sub(r'\s+', ' ', value)
        if len(value) < 10:
            raise ValidationError('Message is too short')
        return value
    
    return value


def is_spam_content(text):
    """Basic spam detection"""
    spam_keywords = [
        'viagra', 'casino', 'lottery', 'winner', 'congratulations',
        'click here', 'free money', 'make money fast', 'get rich quick',
        'urgent response', 'limited time', 'act now'
    ]
    
    text_lower = text.lower()
    spam_count = sum(1 for keyword in spam_keywords if keyword in text_lower)
    
    # Consider it spam if multiple spam keywords are found
    return spam_count >= 2


@vary_on_headers('User-Agent')
def resume(request):
    """Resume page view"""
    # Optimized queries - removed invalid select_related('user')
    education_items = Education.objects.all()
    certifications = Certification.objects.all()
    achievements = Achievement.objects.filter(is_active=True)
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    
    # Organize skills by category with proper mapping
    skills_by_category = {}
    category_mapping = {
        'skill': 'Skills',
        'tools': 'Tools',
        'soft': 'Special Skills',
    }
    
    for skill in skills:
        # Map the category to our template categories
        mapped_category = category_mapping.get(skill.category, skill.category)
        if mapped_category not in skills_by_category:
            skills_by_category[mapped_category] = []
        skills_by_category[mapped_category].append(skill)
    
    context = {
        'education_items': education_items,
        'certifications': certifications,
        'achievements': achievements,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
    }
    
    return render(request, 'main/resume.html', context)


def download_resume(request):
    """Download resume as PDF from uploaded CV or fallback to static file"""
    try:
        # First, try to get the uploaded CV from the first superuser's profile
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            profile, created = UserProfile.objects.get_or_create(user=superuser)
            if profile.cv_document and os.path.exists(profile.cv_document.path):
                response = FileResponse(
                    open(profile.cv_document.path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'attachment; filename="Christopher_Erick_Resume.pdf"'
                return response
    except Exception as e:
        pass
    
    # Fallback to static resume file if no uploaded CV found
    resume_path = os.path.join(settings.MEDIA_ROOT, 'resume.pdf')
    
    if os.path.exists(resume_path):
        response = FileResponse(open(resume_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Christopher_Resume.pdf"'
        return response
    else:
        return HttpResponse('Resume not found. Please upload a CV through the admin panel.', status=404)


def about(request):
    """About page view"""
    return render(request, 'main/about.html')


def icon_test(request):
    """Icon test page for debugging FontAwesome issues"""
    return render(request, 'main/icon_test.html')


@staff_member_required
def security_dashboard(request):
    """Admin-only Security Dashboard with real-time data"""
    # Get time ranges for analysis
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    
    # Get real security metrics
    failed_logins_24h = SecurityEvent.objects.filter(
        event_type='login_failed',
        created_at__gte=last_24h
    ).count()
    
    admin_access_24h = SecurityEvent.objects.filter(
        event_type='admin_access',
        created_at__gte=last_24h
    ).count()
    
    contact_submissions_24h = ContactSubmission.objects.filter(
        created_at__gte=last_24h
    ).count()
    
    suspicious_requests_24h = SecurityEvent.objects.filter(
        event_type='suspicious_request',
        created_at__gte=last_24h
    ).count()
    
    rate_violations_24h = SecurityEvent.objects.filter(
        event_type='rate_limit',
        created_at__gte=last_24h
    ).count()
    
    # Calculate threat level
    threat_score = 0
    if failed_logins_24h > 10:
        threat_score += 3
    elif failed_logins_24h > 5:
        threat_score += 2
    elif failed_logins_24h > 0:
        threat_score += 1
        
    if suspicious_requests_24h > 20:
        threat_score += 3
    elif suspicious_requests_24h > 10:
        threat_score += 2
    elif suspicious_requests_24h > 0:
        threat_score += 1
        
    if rate_violations_24h > 50:
        threat_score += 2
    elif rate_violations_24h > 20:
        threat_score += 1
    
    # Determine threat level
    if threat_score >= 6:
        threat_level = 'CRITICAL'
        threat_color = 'critical'
    elif threat_score >= 4:
        threat_level = 'HIGH'
        threat_color = 'high'
    elif threat_score >= 2:
        threat_level = 'MEDIUM'
        threat_color = 'medium'
    else:
        threat_level = 'LOW'
        threat_color = 'low'
    
    # Get recent security events for timeline
    recent_events = SecurityEvent.objects.filter(
        created_at__gte=last_24h
    ).order_by('-created_at')[:10]
    
    # Get unique IP addresses
    unique_ips_24h = SecurityEvent.objects.filter(
        created_at__gte=last_24h
    ).values('ip_address').distinct().count()
    
    # System status
    system_status = 'SECURE'
    if threat_level in ['HIGH', 'CRITICAL']:
        system_status = 'ALERT'
    elif threat_level == 'MEDIUM':
        system_status = 'MONITORING'
        
    context = {
        'user_profile': {
            'name': PersonalConfig.get_full_name(),
            'email': PersonalConfig.get_email(),
            'tryhackme': PersonalConfig.get_tryhackme_username(),
            'hackthebox': PersonalConfig.get_hackthebox_username(),
            'tagline': PersonalConfig.get_tagline()
        },
        'metrics': {
            'threat_level': threat_level,
            'threat_color': threat_color,
            'threat_score': threat_score,
            'failed_logins': failed_logins_24h,
            'admin_access': admin_access_24h,
            'contact_submissions': contact_submissions_24h,
            'suspicious_requests': suspicious_requests_24h,
            'rate_violations': rate_violations_24h,
            'unique_ips': unique_ips_24h,
            'system_status': system_status
        },
        'recent_events': recent_events,
        'total_events_7d': SecurityEvent.objects.filter(created_at__gte=last_7d).count(),
        'last_updated': now
    }
    
    return render(request, 'main/security_dashboard.html', context)


@staff_member_required
def download_security_report(request):
    """Generate and download a security report of login attempts"""
    import csv
    from django.http import HttpResponse
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="security_report.csv"'
    
    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow([
        'Event Type', 
        'Username', 
        'IP Address', 
        'Login Status', 
        'Description', 
        'Timestamp', 
        'User Agent',
        'Path',
        'Method'
    ])
    
    # Get all security events, ordered by timestamp
    security_events = SecurityEvent.objects.all().order_by('-created_at')
    
    # Write data rows
    for event in security_events:
        login_status = 'Failed' if event.event_type == 'login_failed' else 'Success' if event.event_type == 'login_success' else 'N/A'
        writer.writerow([
            event.get_event_type_display(),
            event.username,
            event.ip_address,
            login_status,
            event.description,
            event.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            event.user_agent,
            event.path,
            event.method
        ])
    
    return response


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for Fly.io
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Portfolio website is running successfully'
    })
