# Cybersecurity Professional Portfolio

A high-performance, security-hardened Django portfolio website optimized for deployment on **Cloudflare** (Cloudflare Tunnel, R2 Storage, WAF & CDN).

## Project Overview

This portfolio website is designed for cybersecurity professionals to showcase their skills, projects, and experience. It features a modern, responsive design with dark/light mode support, rate-limiting security middleware, Cloudflare edge integration, and zero-egress R2 media storage.

## Features

- **Professional Portfolio**: Display skills, experience, education, and certifications
- **Project Showcase**: Highlight cybersecurity projects with detailed writeups and documents
- **Blog Section**: Share knowledge through technical blog posts with view/like analytics
- **Security Audit & Dashboard**: Custom rate-limiting, Cloudflare IP detection, security event logging
- **Cloudflare Integration**: Built for Cloudflare Tunnel (`cloudflared`) & Cloudflare R2 Media Storage
- **Responsive Design**: Modern glassmorphism UI with dark/light theme switching

## Quick Deployment (Cloudflare)

For complete production deployment instructions on Cloudflare, see **[CLOUDFLARE_DEPLOYMENT_GUIDE.md](CLOUDFLARE_DEPLOYMENT_GUIDE.md)**.

```bash
# Copy Cloudflare environment template
cp .env.example .env

# Start stack with Cloudflare Tunnel & PostgreSQL
docker compose up -d --build
```

## Repository Structure

- **`portfolio_site/`**: Core Django settings & WSGI configuration
- **`main/`**, **`portfolio/`**, **`blog/`**: Application modules & views
- **`cloudflared/`**: Cloudflare Tunnel configuration
- **`scripts/`**: Project management, data population & verification scripts
- **`docs/`**: Historical deployment guides and technical reference manuals

## Technology Stack

- **Backend**: Django (Python 3.12)
- **Frontend**: Vanilla CSS / JavaScript, HTML5
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Object Storage**: Cloudflare R2 (S3 compatible)
- **Edge Network**: Cloudflare Tunnel, WAF, DNS, CDN

1. Configure environment variables (your personal information is already preserved):
   ```bash
   # For development
   cp .env.development .env
   
   # For production
   cp .env.production .env
   ```

2. Edit the `.env` file to configure your settings:
   ```bash
   nano .env
   ```
   Your personal information (name, email, phone, location, social media usernames) is already preserved in the environment files.

3. Generate a secure secret key:
   ```bash
   # Using Python
   python generate_secret_key.py
   
   # Using PowerShell (Windows)
   .\generate_secret_key.ps1
   ```

4. Build and start services:
   ```bash
   docker-compose up --build
   ```

5. Run initial setup:
   ```bash
   # Run database migrations
   docker-compose exec web python manage.py migrate
   
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

6. Generate SSL certificates (for development only):
   ```bash
   # On Linux/Mac
   ./generate_cert.sh
   
   # On Windows
   .\generate_cert.ps1
   ```

7. Access the application at http://localhost

## Project Structure

```
RESUME/
├── blog/              # Blog application
├── config/            # Configuration files (Nginx, SSL certificates)
├── main/              # Main application
├── portfolio/         # Portfolio application
├── portfolio_site/    # Django project settings
├── static/            # CSS, JavaScript, images
├── templates/         # Base templates
├── .env               # Environment variables (not in version control)
├── .env.production    # Template for production environment (preserves your information)
├── .env.development   # Template for development environment (preserves your information)
├── .env.backup        # Backup of your original .env file
├── build.sh           # Unix build script for deployment
├── build.bat          # Windows build script for deployment
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Key Components

### Main Application
- Homepage with security arsenal
- About page with professional journey
- Resume page with skills and experience
- Contact page with form
- Security dashboard for monitoring

### Portfolio Application
- Project listing and details
- Technology categorization

### Blog Application
- Blog post listing and details
- Comment system
- Like/dislike functionality

## Customization

### Personal Information
Your personal information is managed through environment variables and is already configured with your details:
- FULL_NAME: Christopher Erick Otieno
- EMAIL: erikchris54@gmail.com
- PHONE: +254758081580
- LOCATION: Nairobi, Kenya
- GITHUB_USERNAME: Christopher-Erick
- TRYHACKME_USERNAME: erikchris54
- HACKTHEBOX_USERNAME: ChristopherErick

### Styling
Modify `static/css/style.css` to change the look and feel.

### Functionality
Update views in `main/views.py`, `portfolio/views.py`, and `blog/views.py` to modify functionality.

## Security Features

- Custom security middleware
- Rate limiting protection
- Suspicious request detection
- Security event logging
- Admin security dashboard

## Deployment

For deployment instructions, see:
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for Render deployment

### Media Files in Production

For production deployments (especially on platforms like Render), this application supports Cloudinary for persistent media storage. See [CLOUDINARY_SETUP_GUIDE.md](CLOUDINARY_SETUP_GUIDE.md) for setup instructions.

Cloudinary integration was successfully configured on September 19, 2025.

### Build Scripts

This project includes platform-specific build scripts to ensure proper deployment across different environments:

- `build.sh` - Unix/Linux build script
- `build.bat` - Windows build script
- `build` - Generic build script (Unix/Linux)

All build scripts have executable permissions set. If you encounter permission issues during deployment, you can use the permission setting scripts:

- `set_permissions.sh` - Unix/Linux permission setting script
- `set_permissions.bat` - Windows permission setting script
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for Railway deployment
- [DOCKER_DEPLOYMENT_GUIDE.md](DOCKER_DEPLOYMENT_GUIDE.md) for Docker deployment

If you've deployed the application and it's missing data, see [FIX_DEPLOYMENT.md](FIX_DEPLOYMENT.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is proprietary and intended for personal use by cybersecurity professionals.

## Contact

For questions about this project, please use the contact form on the website or reach out directly.

---
*Built with Django and designed for cybersecurity professionals*