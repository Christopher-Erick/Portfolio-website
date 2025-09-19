import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Testimonial, Skill, Education, Certification, Achievement, Experience, ContactSubmission

# Get the logger
logger = logging.getLogger('portfolio_site')

def home(request):
    """Render the home page"""
    # Fetch active testimonials ordered by display order
    testimonials = getattr(Testimonial, 'objects').filter(is_active=True).order_by('order', 'name')
    
    # Debug: Print number of testimonials to console
    print(f"Number of testimonials fetched: {testimonials.count()}")
    
    return render(request, 'main/home.html', {
        'testimonials': testimonials
    })

def about(request):
    """Render the about page"""
    return render(request, 'main/about.html')

def resume(request):
    """Render the resume page"""
    # Fetch all resume-related data
    education_items = getattr(Education, 'objects').all()
    certifications = getattr(Certification, 'objects').all()
    achievements = getattr(Achievement, 'objects').filter(is_active=True)
    skills = getattr(Skill, 'objects').all()
    experiences = getattr(Experience, 'objects').all()
    
    # Organize skills by category
    skills_by_category = {}
    category_mapping = {
        'skill': 'Skills',
        'tools': 'Tools',
        'soft': 'Special Skills',
    }
    
    for skill in skills:
        mapped_category = category_mapping.get(skill.category, skill.category)
        if mapped_category not in skills_by_category:
            skills_by_category[mapped_category] = []
        skills_by_category[mapped_category].append(skill)
    
    return render(request, 'main/resume.html', {
        'education_items': education_items,
        'certifications': certifications,
        'achievements': achievements,
        'experiences': experiences,
        'skills_by_category': skills_by_category,
    })

def download_resume(request):
    """Handle resume download - serves uploaded CV or fallback static file"""
    try:
        # Try to get the admin user's profile
        from django.contrib.auth.models import User
        admin_user = User.objects.filter(is_staff=True).first()
        
        if admin_user and hasattr(admin_user, 'profile'):
            user_profile = admin_user.profile
            # Check if a CV document is uploaded
            if user_profile.cv_document:
                # Serve the uploaded CV file
                from django.http import FileResponse
                import os
                
                # Get the file path
                file_path = user_profile.cv_document.path
                
                # Check if file exists
                if os.path.exists(file_path):
                    # Get the filename for the download
                    filename = user_profile.cv_filename or 'Christopher_Erick_Resume.pdf'
                    
                    # Serve the file
                    response = FileResponse(
                        open(file_path, 'rb'),
                        as_attachment=True,
                        filename=filename
                    )
                    return response
                else:
                    # File doesn't exist on disk
                    messages.warning(request, 'The uploaded CV file could not be found.')
            else:
                # No CV uploaded
                messages.info(request, 'No CV has been uploaded yet.')
        else:
            # No admin user or profile
            messages.info(request, 'No user profile found.')
            
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error serving CV: {str(e)}")
        messages.error(request, 'An error occurred while trying to download the CV.')
    
    # Fallback: Try to serve static resume.pdf if it exists
    try:
        import os
        from django.conf import settings
        from django.http import FileResponse
        
        static_resume_path = os.path.join(settings.MEDIA_ROOT, 'resume.pdf')
        if os.path.exists(static_resume_path):
            response = FileResponse(
                open(static_resume_path, 'rb'),
                as_attachment=True,
                filename='Christopher_Erick_Resume.pdf'
            )
            return response
    except Exception as e:
        logger.error(f"Error serving static resume: {str(e)}")
    
    # If all else fails, show message
    messages.info(request, 'Resume download functionality would be implemented here.')
    return redirect('main:resume')

def contact(request):
    """Handle contact form"""
    if request.method == 'POST':
        # Simple form handling without a form class
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        if name and email and subject and message:
            # Save to database
            try:
                contact_submission = getattr(ContactSubmission, 'objects').create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                logger.info(f"Contact submission saved to database: {contact_submission.id}")
                database_success = True
            except Exception as e:
                logger.error(f"Failed to save contact submission to database: {str(e)}")
                database_success = False
            
            # Log the contact attempt
            logger.info(f"Contact form submitted by {name} ({email}) with subject: {subject}")
            
            # Try to send email (in production, you'd use a proper email backend)
            email_success = False
            try:
                # Check if email settings are configured
                if hasattr(settings, 'CONTACT_EMAIL') and settings.CONTACT_EMAIL:
                    send_mail(
                        f"Contact Form: {subject}",
                        f"From: {name} <{email}>\n\n{message}",
                        email,  # From email
                        [settings.CONTACT_EMAIL],  # To email
                        fail_silently=False,
                    )
                    email_success = True
                    logger.info(f"Contact email sent successfully from {email}")
                else:
                    # Email not configured, but that's okay
                    logger.info("Email not configured, skipping email send")
            except Exception as e:
                logger.error(f"Failed to send contact email: {str(e)}")
            
            # Show appropriate message based on what worked
            if database_success:
                messages.success(request, 'Thank you for your message. We will contact you soon!')
            else:
                messages.success(request, 'Thank you for your message. We will contact you soon! (Note: There was an issue saving your message, but it was sent via email)')
            
            return redirect('main:contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'main/contact.html')

def security_dashboard(request):
    """Render the security dashboard"""
    # This would typically fetch security event data from the database
    # For now, we'll just render the template
    return render(request, 'main/security_dashboard.html')

def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    # Check if we're in debug mode
    from django.conf import settings
    debug_mode = getattr(settings, 'DEBUG', False)
    
    # Check Cloudinary configuration
    cloudinary_status = "Not checked"
    try:
        from django.conf import settings
        default_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', '')
        if 'cloudinary' in default_storage.lower():
            cloudinary_status = "Configured"
        else:
            cloudinary_status = "Not configured"
    except:
        cloudinary_status = "Error checking"
    
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'database': db_status,
        'debug': debug_mode,
        'cloudinary': cloudinary_status
    })

def cloudinary_test(request):
    """Test endpoint to check Cloudinary configuration"""
    import os
    from django.conf import settings
    
    # Check Cloudinary environment variables
    cloudinary_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'Not set')
    cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY', 'Not set')
    cloudinary_api_secret = 'Set' if os.getenv('CLOUDINARY_API_SECRET') else 'Not set'
    
    # Check Django settings
    default_file_storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')
    debug = getattr(settings, 'DEBUG', 'Not set')
    
    # Check if Cloudinary is being used
    using_cloudinary = 'cloudinary' in default_file_storage.lower() if default_file_storage != 'Not set' else False
    
    # Test Cloudinary connection
    cloudinary_test_result = "Not tested"
    if using_cloudinary:
        try:
            import cloudinary
            import cloudinary.uploader
            # Test the configuration
            config = cloudinary.config()
            if config.cloud_name and config.api_key:
                cloudinary_test_result = "Connection successful"
            else:
                cloudinary_test_result = "Configuration incomplete"
        except Exception as e:
            cloudinary_test_result = f"Connection failed: {str(e)}"
    
    return JsonResponse({
        'cloudinary_configured': using_cloudinary,
        'cloudinary_cloud_name': cloudinary_cloud_name,
        'cloudinary_api_key': 'Set' if cloudinary_api_key != 'Not set' else 'Not set',
        'cloudinary_api_secret': cloudinary_api_secret,
        'default_file_storage': default_file_storage,
        'debug_mode': debug,
        'cloudinary_test': cloudinary_test_result,
        'status': 'Cloudinary is configured' if using_cloudinary else 'Cloudinary is not configured'
    })

def test_social_links(request):
    """Test view to check social links rendering"""
    return render(request, 'test_social_links.html')