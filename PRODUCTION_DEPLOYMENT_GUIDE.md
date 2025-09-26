# Production Deployment Guide

This guide will help you deploy your portfolio website to production with all the necessary environment variables and configurations.

## Environment Variables

For production deployment, you need to set the following environment variables:

### Django Configuration
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-app-name.onrender.com
ADMIN_URL=secure-admin-path-12345/
```

### Database Configuration
```
DATABASE_URL=postgres://username:password@host:port/database_name
```

### Email Configuration
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_EMAIL=your-email@gmail.com
```

### Cloudinary Configuration
```
CLOUDINARY_CLOUD_NAME=dge5xurfz
CLOUDINARY_API_KEY=172734151545842
CLOUDINARY_API_SECRET=Yry1SKCjiA8ddXCP8lqclK-B9u4
```

### Personal Information
```
FULL_NAME=Christopher Erick Otieno
EMAIL=erikchris54@gmail.com
GITHUB_USERNAME=Christopher-Erick
TRYHACKME_USERNAME=erikchris54
HACKTHEBOX_USERNAME=ChristopherErick
TAGLINE=Building secure digital ecosystems from the ground up — where cybersecurity meets seamless operations, data drives decisions, and complex challenges become elegant solutions.
PHONE=+254758081580
LOCATION=Nairobi, Kenya
```

### Admin Configuration
```
ADMIN_USERNAME=portfolio_admin_x7k9
ADMIN_EMAIL=erikchris54@gmail.com
```

### Security Settings
```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Deployment Platforms

### Render Deployment

1. Go to your Render dashboard
2. Connect your GitHub repository
3. Set up a new Web Service
4. In the "Environment" tab, add all the environment variables listed above
5. Set the build command to: `pip install -r requirements.txt`
6. Set the start command to: `gunicorn portfolio_site.wsgi:application`
7. Deploy!

### Fly.io Deployment

1. Install the Fly.io CLI
2. Run `fly launch` in your project directory
3. Set the environment variables using `fly secrets set`:
   ```
   fly secrets set DEBUG=False
   fly secrets set SECRET_KEY=your-super-secret-key
   fly secrets set CLOUDINARY_CLOUD_NAME=dge5xurfz
   # ... (set all other environment variables)
   ```
4. Deploy with `fly deploy`

### Railway Deployment

1. Go to your Railway dashboard
2. Create a new project
3. Connect your GitHub repository
4. Add a PostgreSQL database
5. In the service settings, add all the environment variables listed above
6. Deploy!

## Post-Deployment Steps

1. **Create a superuser**:
   ```bash
   python manage.py create_production_admin
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Verify Cloudinary integration**:
   - Check that all media files are loading from Cloudinary URLs
   - Verify that the contact form works correctly

## Troubleshooting

### If Images/Writeups Don't Load

1. Check that your Cloudinary environment variables are correctly set
2. Verify that files exist in your Cloudinary account
3. Check that file names match exactly what's in your database

### If Contact Form Doesn't Work

1. Verify that `CONTACT_EMAIL` is set correctly
2. Check email configuration settings
3. Ensure your email provider allows sending emails from your application

### If Admin Panel Is Not Accessible

1. Verify that `ADMIN_URL` is set to a unique path
2. Check that you've created a superuser account
3. Ensure that the admin URL is not blocked by security settings

## Security Notes

- Never commit actual secrets to version control
- Use strong, unique passwords for all accounts
- Regularly update dependencies
- Monitor your application logs for suspicious activity
- Keep your Cloudinary API credentials secure