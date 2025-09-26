# Cloudinary Setup Guide for Django Portfolio

This guide explains how to set up Cloudinary for storing media files in your Django portfolio application deployed on Render.

## Prerequisites

1. A Cloudinary account (free tier available)
2. Your Django application with Cloudinary packages installed

## Step 1: Create a Cloudinary Account

1. Go to [https://cloudinary.com/](https://cloudinary.com/)
2. Click "Sign up for free"
3. Complete the registration process
4. Verify your email address

## Step 2: Get Your Cloudinary Credentials

1. After logging in, go to your Cloudinary dashboard
2. Find your account credentials:
   - Cloud Name (usually displayed prominently)
   - API Key
   - API Secret

## Step 3: Add Environment Variables to Render

1. Go to your Render dashboard
2. Click on your web service
3. Go to the "Environment" tab
4. Add these environment variables:
   ```
   CLOUDINARY_CLOUD_NAME = your_cloud_name
   CLOUDINARY_API_KEY = your_api_key
   CLOUDINARY_API_SECRET = your_api_secret
   ```

## Step 4: Redeploy Your Application

After adding the environment variables, Render will automatically redeploy your application with Cloudinary integration.

## How It Works

The configuration we've added to your settings.py file automatically detects when Cloudinary credentials are available and switches to using Cloudinary for media storage instead of local storage:

```python
if not DEBUG and CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    # Use Cloudinary for media files in production
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

## Benefits

1. **Persistence**: Media files will persist between deployments
2. **Scalability**: Cloudinary provides CDN delivery for better performance
3. **Reliability**: Files are stored in a managed cloud service
4. **Easy Setup**: Simple configuration with environment variables

## Troubleshooting

### If Images Still Don't Appear

1. Check that all three Cloudinary environment variables are set correctly in Render
2. Verify your Cloudinary account is active and not suspended
3. Check Render logs for any Cloudinary-related errors
4. Ensure your Cloudinary account has sufficient quota (free tier includes 25 credits)

### If You Want to Revert to Local Storage

1. Remove the Cloudinary environment variables from Render
2. Redeploy your application
3. The system will automatically fall back to local storage

## Security Notes

- Never commit your Cloudinary credentials to version control
- Use environment variables as we've configured
- The free tier is sufficient for most portfolio applications
- Cloudinary provides good security practices by default