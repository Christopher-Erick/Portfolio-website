# Portfolio Media Files Guide

This guide explains how to properly add media files (images and write-ups) for your portfolio projects.

## Current Issue

The database contains references to media files for portfolio projects, but the actual files don't exist on disk:

1. **Vulnerability Assessment Project**:
   - Image: `projects/VULNERABILITY_ASSEMEMENT.PNG`
   - Write-up: `projects/writeups/SECURITY_ASSESSEMENT.pdf`

2. **SIEM Project**:
   - Image: `projects/splunk.png`
   - Write-up: `projects/writeups/Splunk_Exploring_SPL.pdf`

3. **Malware Analysis Project**:
   - Image: `projects/malware.PNG`
   - Write-up: `projects/writeups/Malware_Analysis.pdf`

## Solution Options

### Option 1: Upload via Django Admin (Recommended)

1. Start your Django server:
   ```bash
   python manage.py runserver
   ```

2. Access the admin panel at `http://127.0.0.1:8000/admin/`

3. Navigate to Portfolio > Projects

4. For each project:
   - Click on the project title to edit it
   - In the "Media" section:
     - Click "Choose File" next to "Featured image" and upload your project image
     - Click "Choose File" next to "Writeup document" and upload your write-up document
   - Click "Save"

### Option 2: Cloudinary Integration (For Production/Render Deployment)

Your application is now configured to use Cloudinary for media storage in production. This ensures that your media files persist between deployments on platforms like Render.

To set up Cloudinary:

1. Create a free account at [https://cloudinary.com/](https://cloudinary.com/)
2. Get your Cloudinary credentials (Cloud Name, API Key, API Secret)
3. Add these as environment variables in your Render deployment:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
4. Redeploy your application

See [CLOUDINARY_SETUP_GUIDE.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/CLOUDINARY_SETUP_GUIDE.md) for detailed instructions.

### Option 2: Add Files to Repository

If you want to commit sample files to the repository:

1. Create the necessary directories:
   ```bash
   mkdir -p static/images
   mkdir -p static/documents
   ```

2. Add your project images to `static/images/`:
   - `static/images/VULNERABILITY_ASSEMEMENT.PNG`
   - `static/images/splunk.png`
   - `static/images/malware.PNG`

3. Add your write-up documents to `static/documents/`:
   - `static/documents/SECURITY_ASSESSEMENT.pdf`
   - `static/documents/Splunk_Exploring_SPL.pdf`
   - `static/documents/Malware_Analysis.pdf`

4. Update the database to point to these files (requires Django shell commands or admin upload).

## File Requirements

### Images
- Supported formats: JPG, PNG, GIF, WEBP
- Recommended size: 800x600px
- Should be relevant to the project content

### Write-ups
- Supported formats: PDF, DOC, DOCX, TXT
- Should contain detailed project information
- Include methodology, findings, and results

## Best Practices

1. Use descriptive filenames without spaces
2. Keep file sizes reasonable (under 5MB each)
3. Ensure images are high quality but optimized
4. Write comprehensive but concise write-ups
5. Include technical details relevant to the project

## Verification

After adding files, verify they display correctly:
1. Visit `http://127.0.0.1:8000/portfolio/` to see the project listing
2. Click on individual projects to view details
3. Check that images display properly
4. Verify write-up links work and documents can be downloaded

## Troubleshooting

If files don't display:
1. Check that the media files exist in the correct location
2. Verify file permissions
3. Ensure `MEDIA_URL` and `MEDIA_ROOT` are correctly configured in settings
4. Restart the Django development server