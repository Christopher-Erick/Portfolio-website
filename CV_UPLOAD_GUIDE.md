# CV Upload and Download Functionality - Admin Panel Guide

## Overview
I've implemented a streamlined CV upload and download system that works exclusively through the Django admin panel. This gives you centralized control and keeps the frontend clean.

## Features Implemented

### 1. **UserProfile Model**
- Created a `UserProfile` model linked to Django's User model
- Includes a `cv_document` field for file uploads
- Supports PDF, DOC, and DOCX files (max 10MB)
- Tracks upload timestamp

### 2. **Enhanced Admin Interface**
- User profiles integrated into Django admin
- Easy CV upload and management
- Download links in admin list view
- File validation and error handling

### 3. **Smart Download System**
- **Download Resume**: Checks for uploaded CV first, falls back to static file
- Professional filename: "Christopher_Erick_Resume.pdf"
- Works across all download buttons on your site

## How to Use

### Upload CV (Admin Panel Only):
1. **Access Django Admin**: Go to `http://127.0.0.1:8000/admin`
   - Username: `admin`
   - Password: `admin123`

2. **Navigate to User Profiles**:
   - Click on "User profiles" in the admin
   - Find your user profile (admin)
   - Click to edit

3. **Upload CV**:
   - Use the "Cv document" field to upload your CV
   - Supports PDF, DOC, DOCX files (max 10MB)
   - Save the profile

4. **Manage CV**:
   - View upload timestamp
   - Download current CV directly from admin
   - Replace with new versions anytime

### For Visitors:
- **Download CV**: Any "Download Resume" button on your site will serve your uploaded CV
- If no CV is uploaded, it falls back to looking for `media/resume.pdf`
- Clean, professional download experience

## Admin Features:
- ✅ **Easy Upload**: Simple file field in admin interface
- ✅ **File Validation**: Automatic validation of file types and sizes
- ✅ **Download Links**: Direct download links in admin list view
- ✅ **Upload Tracking**: See when CV was last updated
- ✅ **User Management**: Linked to user accounts for multi-user sites

## File Structure:

### Files Created/Modified:
- `main/models.py` - Added UserProfile model
- `main/admin.py` - Enhanced admin interface with CV management
- `main/views.py` - Smart download logic
- `main/migrations/0002_userprofile.py` - Database migration

### Files Removed:
- `main/forms.py` - No longer needed (admin handles forms)
- `templates/main/upload_cv.html` - Removed frontend upload page
- Frontend upload sections from about.html - Simplified interface

## Security Features:
- ✅ File type validation (PDF, DOC, DOCX only)
- ✅ File size limits (10MB maximum)
- ✅ Admin-only access for uploads (more secure)
- ✅ Secure file handling with Django's FileField

## Benefits of Admin-Only Approach:
- **Simpler**: No frontend forms to maintain
- **Secure**: Only admin users can upload CVs
- **Centralized**: All management in one place
- **Clean Frontend**: About page stays focused on content
- **Professional**: Visitors only see download functionality

## Quick Start:
1. Login to admin panel
2. Go to "User profiles"
3. Edit your admin user profile
4. Upload your CV in the "Cv document" field
5. Save - your CV is now available for download across the site!

The system automatically handles the rest - any "Download Resume" button will now serve your uploaded CV file.