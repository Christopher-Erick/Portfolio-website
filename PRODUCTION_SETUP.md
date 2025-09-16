# Production Setup Guide

## Security Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Basic Configuration
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here

# Domain Configuration
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration (for production)
DATABASE_URL=postgres://user:password@localhost:5432/portfolio_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=your-email@yourdomain.com
CONTACT_EMAIL=your-contact-email@yourdomain.com

# Security Configuration
ADMIN_URL=your-secure-admin-path-change-this/

# Personal Information
FULL_NAME=Your Full Name
EMAIL=your-email@yourdomain.com
GITHUB_USERNAME=your-github-username
TRYHACKME_USERNAME=your-tryhackme-username
HACKTHEBOX_USERNAME=your-hackthebox-username
TAGLINE=Your professional tagline
PHONE=+1234567890
LOCATION=Your Location

# Admin Configuration
ADMIN_USERNAME=your-admin-username
ADMIN_EMAIL=your-admin-email@yourdomain.com

# Additional Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Security Checklist

1. [ ] Set DEBUG=False
2. [ ] Configure proper ALLOWED_HOSTS
3. [ ] Use a strong SECRET_KEY
4. [ ] Enable secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
5. [ ] Enable HTTPS redirect (SECURE_SSL_REDIRECT)
6. [ ] Configure HSTS (SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, SECURE_HSTS_PRELOAD)
7. [ ] Enable security middleware
8. [ ] Secure sensitive files (.env, database)
9. [ ] Configure database for production
10. [ ] Set up proper email backend
11. [ ] Customize ADMIN_URL
12. [ ] Run security checks: `python manage.py check --deploy`

### Running Security Tests

```bash
# Verify security configuration
python verify_security.py

# Run security compliance tests
python security_compliance_test.py

# Run file cleanup tests
python file_cleanup_test.py

# Run complete security audit
python complete_security_audit.py
```

### Deployment Commands

```bash
# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Run production server
python manage.py runserver 0.0.0.0:8000
```

### Additional Security Measures

1. Use a reverse proxy (nginx) in production
2. Configure proper SSL certificates
3. Set up database backups
4. Monitor security logs regularly
5. Regularly update dependencies
6. Run vulnerability scans
7. Implement proper access controls