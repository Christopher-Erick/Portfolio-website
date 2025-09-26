# Media File Re-upload Instructions

Now that Cloudinary is properly configured on your Render deployment, you need to re-upload your media files so they are stored in Cloudinary rather than locally.

## Steps to Re-upload Media Files

### 1. Access the Django Admin

1. Visit your admin panel at `https://christopher-erick-otieno-portfolio.onrender.com/secure-admin-path-12345/` (or your custom admin URL)
2. Log in with your admin credentials

### 2. Re-upload Files for Each Project

Navigate to Portfolio > Projects and for each project:

1. Click on the project title to edit it
2. In the "Media" section:
   - Click "Choose File" next to "Featured image" and select your project image
   - Click "Choose File" next to "Writeup document" and select your write-up document
3. Scroll to the bottom and click "Save"

### 3. Projects That Need Media Files

Here are the projects that need media files:

1. **SIEM Log Analysis with Splunk SPL - Advanced Query Techniques**
   - Featured image: splunk.png
   - Write-up document: Splunk_Exploring_SPL.pdf

2. **Enterprise Network Penetration Testing**
   - Featured image: pentest.png (or similar)
   - Write-up document: enterprise_network_pentest.pdf (or similar)

3. **Web Application Security Assessment**
   - Featured image: web_app_security.png (or similar)
   - Write-up document: web_app_security_assessment.pdf (or similar)

4. **Security Automation & Incident Response Scripts**
   - Featured image: security_automation.png (or similar)
   - Write-up document: security_automation_scripts.pdf (or similar)

### 4. Verification

After re-uploading:
1. Visit your portfolio pages to verify images display correctly
2. Check that write-up documents are downloadable
3. Confirm that the URLs for media files now point to Cloudinary rather than local storage

## Important Notes

- Files uploaded before Cloudinary configuration will not be automatically migrated
- Only newly uploaded files will be stored in Cloudinary
- Existing database references to old file paths will be updated when you re-upload files
- Make sure to use descriptive filenames without spaces for better compatibility

## Troubleshooting

If files still don't display correctly after re-upload:
1. Check Render logs for any Cloudinary-related errors
2. Verify that all Cloudinary environment variables are correctly set in Render
3. Ensure the redeployment completed successfully
4. Check that your Cloudinary account has sufficient quota

## What Happens After Re-upload

Once you re-upload your files:
- Images will be stored in your Cloudinary account
- Write-up documents will be stored in your Cloudinary account
- Media URLs will automatically point to Cloudinary
- Files will persist between future deployments
- Your portfolio will work correctly on Render