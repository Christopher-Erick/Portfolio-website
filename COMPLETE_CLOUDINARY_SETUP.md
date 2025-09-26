# Complete Cloudinary Setup Guide

Follow these steps to complete your Cloudinary integration:

## Step 1: Get Your Cloudinary Credentials

1. Go to https://cloudinary.com/console
2. Sign in to your Cloudinary account (or create one if you haven't already)
3. On your dashboard, find these values:
   - **Cloud Name**: Displayed prominently at the top
   - **API Key**: Found in the Account Details section
   - **API Secret**: Found in the Account Details section (click to reveal)

## Step 2: Update Your Environment File

Edit the `.env.production` file in your project directory and replace these placeholder values:

```
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

With your actual Cloudinary credentials. For example:

```
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=myportfolio123
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

## Step 3: Verify Your Cloudinary Setup

After updating the credentials, test the configuration:

```bash
python load_env_and_test.py
```

You should see:
```
✓ Cloudinary is properly configured!
```

## Step 4: Update Your Project Media URLs

Once Cloudinary is properly configured, run:

```bash
python manage.py update_cloudinary_urls
```

This will update all your project media files to point to the correct Cloudinary URLs.

## Step 5: Deploy Your Changes

If you're deploying to Render or another platform, make sure to set the same environment variables there:

```
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

## Troubleshooting

### If Files Still Don't Show Up

1. Check that your files are actually uploaded to Cloudinary in the correct folders:
   - Writeup documents should be in a folder called `writeups`
   - Images should be in a folder called `writeupsimages`

2. Verify the file names match exactly what's in your database

3. Check your Render/Fly.io logs for any Cloudinary-related errors

### Manual Verification

You can manually verify a file exists in Cloudinary by accessing this URL:
```
https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/writeups/YOUR_FILENAME.pdf
```

Replace `YOUR_CLOUD_NAME` with your actual Cloud Name and `YOUR_FILENAME.pdf` with the actual file name.