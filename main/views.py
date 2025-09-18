import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .models import Testimonial, Skill, Education, Certification, Achievement, Experience

# Get the logger
logger = logging.getLogger('portfolio_site')

def home(request):
    """Render the home page"""
    # Fetch active testimonials ordered by display order
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order', 'name')
    
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
    education_items = Education.objects.all()
    certifications = Certification.objects.all()
    achievements = Achievement.objects.filter(is_active=True)
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    
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
    """Handle resume download"""
    # In a real implementation, this would serve the actual resume file
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
            # Log the contact attempt
            logger.info(f"Contact form submitted by {name} ({email}) with subject: {subject}")
            
            # Send email (in production, you'd use a proper email backend)
            try:
                send_mail(
                    f"Contact Form: {subject}",
                    f"From: {name} <{email}>\n\n{message}",
                    email,  # From email
                    [settings.CONTACT_EMAIL],  # To email
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message. We will contact you soon!')
                logger.info(f"Contact email sent successfully from {email}")
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
                logger.error(f"Failed to send contact email: {str(e)}")
            
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
    """Health check endpoint for deployment platforms"""
    return render(request, 'main/health.html')

def test_social_links(request):
    """Test view to check social links rendering"""
    return render(request, 'test_social_links.html')