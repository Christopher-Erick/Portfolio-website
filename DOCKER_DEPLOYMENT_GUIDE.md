# Docker Deployment Guide

This guide explains how to deploy the cybersecurity portfolio website using Docker and Docker Compose.

## Prerequisites

1. Docker installed on your system
2. Docker Compose installed on your system
3. OpenSSL (for generating self-signed certificates in development)

## Directory Structure

```
project/
├── Dockerfile
├── docker-compose.yml
├── .env (environment variables)
├── .env.production (template for production)
├── .env.development (template for development)
├── .env.backup (backup of your original .env file)
├── config/
│   ├── nginx/
│   │   └── nginx.conf
│   └── certs/
│       ├── cert.pem (generated)
│       ├── key.pem (generated)
│       └── README.md
├── generate_cert.sh (Linux/Mac)
├── generate_cert.ps1 (Windows)
├── generate_secret_key.py (Python script)
├── generate_secret_key.ps1 (PowerShell script)
└── ... (other project files)
```

## Deployment Steps

### 1. Environment Configuration

Copy the appropriate environment file:

**For Development:**
```bash
cp .env.development .env
```

**For Production:**
```bash
cp .env.production .env
```

Edit the `.env` file to configure your settings:
```bash
nano .env
```

Your personal information is already preserved in the environment files:
- Full Name: Christopher Erick Otieno
- Email: erikchris54@gmail.com
- Phone: +254758081580
- Location: Nairobi, Kenya
- GitHub Username: Christopher-Erick
- TryHackMe Username: erikchris54
- HackTheBox Username: ChristopherErick

Generate a secure secret key:
```bash
# Using Python
python generate_secret_key.py

# Using PowerShell (Windows)
.\generate_secret_key.ps1
```

### 2. Build and Start Services

From the project root directory, run:

```bash
docker-compose up --build
```

This will:
- Build the Django application image
- Start the PostgreSQL database
- Start the Nginx web server
- Start the Gunicorn application server

### 3. Generate SSL Certificates (Development Only)

For development purposes, you can generate self-signed certificates:

**On Linux/Mac:**
```bash
./generate_cert.sh
```

**On Windows:**
```powershell
.\generate_cert.ps1
```

**Note:** For production, use certificates from a trusted Certificate Authority.

### 4. Run Initial Setup

After the containers are running, run the initial setup:

```bash
# Run database migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

Once the containers are running, you can access the application at:
- http://localhost
- https://localhost (if SSL certificates are configured)

### 6. Environment Variables

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

### 7. Production Deployment

For production deployment, see [PRODUCTION_DEPLOYMENT.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/PRODUCTION_DEPLOYMENT.md) for detailed instructions on:

- Server preparation
- SSL certificate setup with Let's Encrypt
- Security hardening
- Monitoring and maintenance
- Backup and restore procedures

## Useful Docker Commands

### View Logs
```bash
docker-compose logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

### Execute Commands in Containers
```bash
# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput

# Access the database
docker-compose exec db psql -U postgres
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Images
```bash
docker-compose build
docker-compose up --build
```

## Health Checks

The Docker configuration includes health checks for both the web application and database:

- Web service: Checks if the application responds to HTTP requests
- Database service: Checks if PostgreSQL is ready to accept connections

## Troubleshooting

### Permission Issues
If you encounter permission issues, especially on Linux, you may need to adjust file permissions:

```bash
chmod +x generate_cert.sh
chmod 600 .env
```

### Port Conflicts
If ports 80 or 443 are already in use, you can modify the port mappings in docker-compose.yml:

```yaml
nginx:
  ports:
    - "8080:80"
    - "8443:443"
```

### Database Issues
If you need to reset the database:

```bash
docker-compose down -v  # This removes volumes including the database
docker-compose up
```

## Customization

### Nginx Configuration
You can modify the Nginx configuration in `config/nginx/nginx.conf` to:
- Add custom headers
- Configure caching
- Set up redirects
- Add additional security headers

### Django Settings
The Django application uses environment variables for configuration. You can modify these in the `.env` file.

## Security Considerations

1. **Secrets Management**: Never commit secrets to version control. Use environment files.

2. **Network Security**: Services are isolated in a Docker network and not exposed unnecessarily.

3. **File Permissions**: The application runs as a non-root user inside the container.

4. **Updates**: Regularly update base images and dependencies.

5. **Health Checks**: Built-in health checks monitor service availability.

This Docker setup provides a production-ready deployment configuration for the cybersecurity portfolio website while preserving all your personal information.