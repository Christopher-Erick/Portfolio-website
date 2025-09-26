# Fixing Cloudinary Integration for Portfolio Media Files

This guide will help you fix the Cloudinary integration for your portfolio project media files (images and writeups).

## Prerequisites

1. Make sure you have uploaded your files to Cloudinary:
   - Writeup documents should be in a folder called `writeups`
   - Images should be in a folder called `writeupsimages`

2. Make sure your Cloudinary environment variables are set:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

## Step 1: Check Current Project Media Status

First, let's see the current status of all project media files:

```bash
python manage.py list_project_media
```

This will show you which projects have local files vs. Cloudinary URLs.

## Step 2: Run the Cloudinary Configuration Check

Check if Cloudinary is properly configured:

```bash
python check_cloudinary_config.py
```

## Step 3: Update Media File URLs

If your files are already uploaded to Cloudinary but the database still contains local paths, run:

```bash
python manage.py update_cloudinary_urls
```

This command will update all local file paths to point to your Cloudinary URLs.

## Step 4: Alternative - Migrate Local Files to Cloudinary

If you have local files that need to be uploaded to Cloudinary, use:

```bash
python manage.py migrate_media_to_cloudinary
```

## Troubleshooting

### If Files Still Don't Show Up

1. Check that your Cloudinary environment variables are correctly set in your deployment environment (Render, etc.)

2. Verify the folder structure in your Cloudinary account matches what the script expects:
   - Writeup documents in `writeups` folder
   - Images in `writeupsimages` folder

3. Check the Render logs for any Cloudinary-related errors.

### Manual URL Update

If the automated commands don't work, you can manually update the URLs in the Django admin:

1. Go to your Django admin panel
2. Navigate to Portfolio > Projects
3. For each project, update the Featured Image and Writeup Document fields with the correct Cloudinary URLs:
   - Featured Image: `https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/writeupsimages/FILENAME.EXT`
   - Writeup Document: `https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/writeups/FILENAME.EXT`

## Cloudinary URL Format

The expected Cloudinary URL format is:
```
https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/FOLDER_NAME/FILENAME.EXT
```

For your setup:
- Images: `https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/writeupsimages/`
- Writeups: `https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/writeups/`

Replace `YOUR_CLOUD_NAME` with your actual Cloudinary cloud name.