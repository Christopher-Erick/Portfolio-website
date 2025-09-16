# Docker Setup for Cybersecurity Portfolio Website

This directory contains all the necessary files to run the cybersecurity portfolio website in Docker containers.

## Quick Start

1. **Configure environment variables:**
   ```bash
   # For development (preserves your existing information)
   cp .env .env.backup  # Backup your current .env file
   cp .env.development .env
   
   # For production (preserves your existing information)
   cp .env .env.backup  # Backup your current .env file
   cp .env.production .env
   ```

2. **Edit the `.env` file to configure your settings:**
   ```bash
   nano .env
   ```
   Your personal information (name, email, phone, location, social media usernames) is already preserved in the environment files.

3. **Generate a secure secret key:**
   ```bash
   # Using Python
   python generate_secret_key.py
   
   # Using PowerShell (Windows)
   .\generate_secret_key.ps1
   ```

4. **Build and start the services:**
   ```bash
   docker-compose up --build
   ```

5. **Run initial setup:**
   ```bash
   # Run database migrations
   docker-compose exec web python manage.py migrate
   
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

6. **Generate SSL certificates (for development only):**
   ```bash
   # On Linux/Mac
   ./generate_cert.sh
   
   # On Windows
   .\generate_cert.ps1
   ```

7. **Access the application:**
   - http://localhost
   - https://localhost (after generating certificates)

## Files Overview

- [Dockerfile](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/Dockerfile): Defines the Django application image
- [docker-compose.yml](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/docker-compose.yml): Defines all services (web, db, nginx)
- [.env](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/.env): Environment variables (not in version control)
- [.env.production](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/.env.production): Template for production environment (preserves your information)
- [.env.development](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/.env.development): Template for development environment (preserves your information)
- [.env.backup](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/.env.backup): Backup of your original .env file
- [config/nginx/nginx.conf](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/config/nginx/nginx.conf): Nginx configuration
- [config/certs/](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/config/certs): SSL certificates directory
- [generate_cert.sh](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/generate_cert.sh): Script to generate self-signed certificates (Linux/Mac)
- [generate_cert.ps1](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/generate_cert.ps1): Script to generate self-signed certificates (Windows)
- [generate_secret_key.py](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/generate_secret_key.py): Script to generate Django secret key (Python)
- [generate_secret_key.ps1](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/generate_secret_key.ps1): Script to generate Django secret key (PowerShell)
- [init_project.sh](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/init_project.sh): Initialization script (Linux/Mac)
- [init_project.ps1](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/init_project.ps1): Initialization script (Windows)
- [docker_health_check.sh](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/docker_health_check.sh): Health check script (Linux/Mac)
- [docker_health_check.ps1](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/docker_health_check.ps1): Health check script (Windows)
- [DOCKER_DEPLOYMENT_GUIDE.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/DOCKER_DEPLOYMENT_GUIDE.md): Comprehensive deployment guide
- [PRODUCTION_DEPLOYMENT.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/PRODUCTION_DEPLOYMENT.md): Production deployment guide

## Services

1. **web**: Django application served by Gunicorn
2. **db**: PostgreSQL database
3. **nginx**: Reverse proxy and static file server

## Volumes

- `postgres_data`: Persistent database storage
- `static_volume`: Django static files
- `media_volume`: User uploaded media files
- `./logs`: Application logs

## Environment Variables

The application uses environment variables for configuration. Your personal information is preserved in these variables:

- `FULL_NAME`: Your full name (Christopher Erick Otieno)
- `EMAIL`: Your email address (erikchris54@gmail.com)
- `PHONE`: Your phone number (+254758081580)
- `LOCATION`: Your location (Nairobi, Kenya)
- `GITHUB_USERNAME`: Your GitHub username (Christopher-Erick)
- `TRYHACKME_USERNAME`: Your TryHackMe username (erikchris54)
- `HACKTHEBOX_USERNAME`: Your HackTheBox username (ChristopherErick)
- `TAGLINE`: Your professional tagline

Additional configuration variables:
- `SECRET_KEY`: Django secret key (generate a secure one)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `POSTGRES_PASSWORD`: Secure password for the PostgreSQL database
- Email settings for contact form functionality

## Production Deployment

For production deployment, see [PRODUCTION_DEPLOYMENT.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/PRODUCTION_DEPLOYMENT.md) for detailed instructions on:

- Server preparation
- SSL certificate setup with Let's Encrypt
- Security hardening
- Monitoring and maintenance
- Backup and restore procedures

## Troubleshooting

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Ensure Docker and Docker Compose are properly installed
3. Verify port availability (80 and 443)
4. Check file permissions, especially for SSL certificates
5. Ensure environment variables are properly configured

For more detailed information, refer to:
- [DOCKER_DEPLOYMENT_GUIDE.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/DOCKER_DEPLOYMENT_GUIDE.md) for general Docker usage
- [PRODUCTION_DEPLOYMENT.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/PRODUCTION_DEPLOYMENT.md) for production deployment