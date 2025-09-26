# Railway Deployment Guide

## Prerequisites

1. A Railway account
2. A PostgreSQL database on Railway
3. Cloudinary account credentials

## Deployment Steps

### 1. Create a New Railway Project

1. Go to [Railway.app](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your portfolio repository

### 2. Configure Environment Variables

In your Railway project settings, add the following environment variables:

#### Database Configuration
```
DATABASE_URL=your-railway-postgresql-database-url
```

#### Cloudinary Configuration
```
CLOUDINARY_CLOUD_NAME=dge5xurfz
CLOUDINARY_API_KEY=172734151545842
CLOUDINARY_API_SECRET=Yry1SKCjiA8ddXCP8lqclK-B9u4
```

#### Django Configuration
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-railway-domain.railway.app
ADMIN_URL=secure-admin-path-12345/
```

#### Email Configuration (Optional)
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

#### Personal Information
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

### 3. Configure Build Settings

Railway will automatically detect and use your build script. The [build](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\build) file includes all necessary steps:

```bash
#!/bin/bash
# exit on error
set -o errexit

# Create logs directory if it doesn't exist
echo "Creating logs directory if it doesn't exist..."
mkdir -p logs

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create cache table for database cache (fallback if Redis is not available)
echo "Creating cache table..."
python manage.py createcachetable || echo "Failed to create cache table, continuing..."

# Populate database with initial data
echo "Populating database with initial data..."
python post_deploy.py

echo "Build completed successfully!"
```

### 4. Deploy

1. Railway will automatically start the deployment process
2. The [post_deploy.py](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\post_deploy.py) script will:
   - Run database migrations
   - Populate the database with initial data
   - Update all project media files with Cloudinary URLs

### 5. Create a Superuser (Optional)

After deployment, you can create a superuser account:

```bash
railway run python manage.py createsuperuser
```

## Troubleshooting

### If Media Files Don't Load

1. Check that all environment variables are correctly set
2. Verify that the Cloudinary credentials are correct
3. Check the Railway logs for any errors

### If Database Connection Fails

1. Verify that the DATABASE_URL is correct
2. Ensure your PostgreSQL database is properly configured
3. Check Railway logs for connection errors

### If Static Files Don't Load

1. Check that the build process completed successfully
2. Verify that static files were collected properly
3. Check that Whitenoise is properly configured

## Post-Deployment Verification

After deployment, verify that everything is working:

1. Visit your site and check that all images load correctly
2. Test the contact form
3. Verify that the admin panel is accessible
4. Check that all project writeups are downloadable

## Updates

To update your site:

1. Push changes to your GitHub repository
2. Railway will automatically redeploy
3. The [post_deploy.py](file://c:\Users\CHRISTOPHER\Desktop\project\RESUME\post_deploy.py) script will run automatically to update the database