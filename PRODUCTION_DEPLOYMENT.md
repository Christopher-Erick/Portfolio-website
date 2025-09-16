# Production Deployment Guide

This guide explains how to deploy the cybersecurity portfolio website in a production environment using Docker and Docker Compose.

## Prerequisites

1. Docker installed on your server
2. Docker Compose installed on your server
3. Domain name configured to point to your server
4. SSL certificates (Let's Encrypt or other CA)

## Production Deployment Steps

### 1. Server Preparation

1. **Update your system**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Docker and Docker Compose**:
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Add your user to the docker group**:
   ```bash
   sudo usermod -aG docker $USER
   ```

### 2. Application Setup

1. **Clone or copy the application** to your server:
   ```bash
   git clone <your-repository-url> /opt/portfolio
   cd /opt/portfolio
   ```

2. **Generate a secure secret key**:
   ```bash
   # Using Python
   python setup_production.py
   
   # Using PowerShell (Windows)
   .\setup_production.ps1
   ```

3. **Update the production environment file**:
   ```bash
   cp .env.production .env
   nano .env
   ```
   
   Update the following variables:
   - `SECRET_KEY`: Use the generated key from .secret_key file
   - `ALLOWED_HOSTS`: Add your domain names
   - `POSTGRES_PASSWORD`: Set a secure database password
   - Email settings: Update with your email provider settings

### 3. SSL Certificate Setup

For production, you should use certificates from a trusted CA like Let's Encrypt:

1. **Install Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificates**:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Copy certificates to the config directory**:
   ```bash
   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem config/certs/cert.pem
   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem config/certs/key.pem
   sudo chown $USER:$USER config/certs/*.pem
   ```

### 4. Build and Deploy

1. **Build the Docker images**:
   ```bash
   docker-compose build
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Run initial database migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser** (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Collect static files**:
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

### 5. Post-Deployment Configuration

1. **Set up log rotation**:
   Create `/etc/logrotate.d/portfolio`:
   ```bash
   /opt/portfolio/logs/*.log {
       daily
       missingok
       rotate 52
       compress
       delaycompress
       notifempty
       create 644 root root
   }
   ```

2. **Set up automatic backups**:
   Create a backup script and cron job to regularly backup your database and media files.

3. **Monitor the application**:
   ```bash
   docker-compose logs -f
   ```

## Environment Variables

The following environment variables should be configured in the `.env` file:

- `SECRET_KEY`: Django secret key (generate a secure one using setup script)
- `DEBUG`: Should be `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `POSTGRES_PASSWORD`: Secure password for the PostgreSQL database
- Email settings for contact form functionality:
  - `EMAIL_HOST`: SMTP server
  - `EMAIL_PORT`: SMTP port
  - `EMAIL_USE_TLS`: Whether to use TLS
  - `EMAIL_HOST_USER`: SMTP username
  - `EMAIL_HOST_PASSWORD`: SMTP password
  - `CONTACT_EMAIL`: Email address for contact form

## Security Considerations

1. **File Permissions**: Ensure sensitive files have appropriate permissions:
   ```bash
   chmod 600 .env
   chmod 600 config/certs/*.pem
   ```

2. **Firewall**: Configure a firewall to only allow necessary ports:
   ```bash
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

3. **Regular Updates**: Regularly update your system and Docker images.

4. **Monitoring**: Set up monitoring for your application and server.

## Maintenance

### Updating the Application

1. **Pull the latest code**:
   ```bash
   git pull
   ```

2. **Rebuild and restart services**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Run migrations if needed**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

### Backup and Restore

1. **Backup database**:
   ```bash
   docker-compose exec db pg_dump -U postgres postgres > backup.sql
   ```

2. **Restore database**:
   ```bash
   docker-compose exec -T db psql -U postgres postgres < backup.sql
   ```

## Troubleshooting

### Common Issues

1. **Permission denied errors**: Check file permissions and user groups.

2. **Database connection issues**: Verify database credentials and network connectivity.

3. **SSL certificate issues**: Ensure certificates are properly configured and not expired.

4. **Nginx configuration errors**: Check the Nginx configuration file for syntax errors:
   ```bash
   docker-compose exec nginx nginx -t
   ```

### Useful Commands

- **View logs**: `docker-compose logs -f`
- **View running containers**: `docker-compose ps`
- **Execute commands in containers**: `docker-compose exec <service> <command>`
- **Stop services**: `docker-compose down`
- **Restart services**: `docker-compose restart`

## Production Readiness Checklist

Use the [PRODUCTION_CHECKLIST.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/PRODUCTION_CHECKLIST.md) file to ensure your application is fully ready for production:

1. ✅ Generate secure SECRET_KEY
2. ✅ Set secure POSTGRES_PASSWORD
3. ✅ Configure ALLOWED_HOSTS with your domain
4. ✅ Set up SSL certificates
5. ✅ Configure email settings
6. ✅ Test all application functionality
7. ✅ Set up monitoring and logging
8. ✅ Implement backup strategy

This production deployment guide provides a solid foundation for running your cybersecurity portfolio website in a production environment with proper security and performance considerations.