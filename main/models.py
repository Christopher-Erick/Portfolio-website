from django.db import models
from django.contrib.auth.models import User
from .validators import validate_cv_upload
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cv_document = models.FileField(
        upload_to='cv/', 
        blank=True, 
        null=True, 
        help_text='Upload your CV/Resume document (PDF, DOC, DOCX)',
        validators=[validate_cv_upload]
    )
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    @property
    def cv_filename(self):
        if self.cv_document:
            return os.path.basename(self.cv_document.name)
        return None


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} - {self.subject}'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('skill', 'Skills'),
        ('tools', 'Tools'),
        ('soft', 'Soft Skills'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(help_text='Proficiency level from 1-100')
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'


class Experience(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text='Comma-separated list of technologies')
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f'{self.position} at {self.company}'
    
    @property
    def is_current(self):
        return self.end_date is None


class Education(models.Model):
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-graduation-cap', help_text='Font Awesome icon class')
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f'{self.degree} from {self.institution}'


class Certification(models.Model):
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True, help_text='Leave empty if certification does not expire')
    credential_id = models.CharField(max_length=100, blank=True, help_text='Certification ID or badge number')
    credential_url = models.URLField(blank=True, help_text='URL to verify certification')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-certificate', help_text='Font Awesome icon class')
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f'{self.name} - {self.issuing_organization}'
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-trophy', help_text='Font Awesome icon class (e.g., fas fa-shield-alt, fas fa-bug, fas fa-code)')
    technologies = models.CharField(max_length=300, blank=True, help_text='Comma-separated list of technologies/tools used (e.g., Burp Suite, ISO 27001, Kali Linux, Metasploit, NIST, Nessus, Nmap, OWASP)')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True, help_text='Uncheck to hide this achievement')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    @property
    def tech_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []


class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text='Full name of the person giving testimonial')
    position = models.CharField(max_length=100, help_text='Job title or role')
    company = models.CharField(max_length=100, help_text='Company or organization name')
    content = models.TextField(help_text='The testimonial content/quote')
    
    # Settings for display
    is_active = models.BooleanField(default=True, help_text='Uncheck to hide this testimonial')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers appear first)')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f'{self.name} - {self.company}'
    
    @property
    def initials(self):
        """Generate initials from the person's name"""
        name_parts = self.name.split()
        if len(name_parts) >= 2:
            return f"{name_parts[0][0].upper()}{name_parts[-1][0].upper()}"
        elif len(name_parts) == 1:
            return name_parts[0][:2].upper()
        return "UN"
    
    @property
    def short_content(self):
        """Return shortened content for admin display"""
        return self.content[:100] + "..." if len(self.content) > 100 else self.content


class SecurityEvent(models.Model):
    """Model to track security events and login attempts"""
    EVENT_TYPES = [
        ('login_failed', 'Failed Login Attempt'),
        ('login_success', 'Successful Login'),
        ('admin_access', 'Admin Panel Access'),
        ('contact_submission', 'Contact Form Submission'),
        ('rate_limit', 'Rate Limit Violation'),
        ('suspicious_request', 'Suspicious Request'),
        ('file_upload', 'File Upload'),
        ('security_scan', 'Security Scan Detected'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='low')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    username = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    path = models.CharField(max_length=500, blank=True)
    method = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['severity', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_event_type_display()} from {self.ip_address} at {self.created_at}"
    
    @classmethod
    def log_event(cls, event_type, ip_address, description, severity='low', **kwargs):
        """Convenience method to log security events"""
        return cls.objects.create(
            event_type=event_type,
            ip_address=ip_address,
            description=description,
            severity=severity,
            **kwargs
        )