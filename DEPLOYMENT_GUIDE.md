# Deployment Guide

## Prerequisites

Before deploying this Django application, ensure you have:
- Python 3.8 or higher
- pip (Python package installer)
- A web server (Apache, Nginx, or similar)
- A database (SQLite, PostgreSQL, MySQL)
- Git (for version control)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd RESUME
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment variables:
   Create a `.env` file in the project root with:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Test the application:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### Using Gunicorn and Nginx (Recommended)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Test Gunicorn:
   ```bash
   gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:8000
   ```

3. Create a Gunicorn configuration file (`gunicorn.conf.py`):
   ```python
   bind = "127.0.0.1:8000"
   workers = 3
   user = "your-user"
   group = "your-group"
   logfile = "/var/log/gunicorn/error.log"
   loglevel = "info"
   ```

4. Create a systemd service file (`/etc/systemd/system/portfolio.service`):
   ```ini
   [Unit]
   Description=Portfolio Django Application
   After=network.target

   [Service]
   User=your-user
   Group=your-group
   WorkingDirectory=/path/to/RESUME
   ExecStart=/path/to/venv/bin/gunicorn --config gunicorn.conf.py portfolio_site.wsgi:application
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. Configure Nginx:
   Create `/etc/nginx/sites-available/portfolio`:
   ```
   server {
       listen 80;
       server_name yourdomain.com;

       location /static/ {
           alias /path/to/RESUME/staticfiles/;
       }

       location /media/ {
           alias /path/to/RESUME/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

6. Enable the Nginx site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. Start the Gunicorn service:
   ```bash
   sudo systemctl start portfolio
   sudo systemctl enable portfolio
   ```

### Using Docker (Alternative)

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "portfolio_site.wsgi:application"]
   ```

2. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "8000:8000"
       environment:
         - DEBUG=False
         - SECRET_KEY=your-secret-key
         - ALLOWED_HOSTS=yourdomain.com
       volumes:
         - static_volume:/app/staticfiles
         - media_volume:/app/media

   volumes:
     static_volume:
     media_volume:
   ```

3. Build and run:
   ```bash
   docker-compose up -d
   ```

## Database Configuration

### SQLite (Default - Development)
No additional configuration needed for development.

### PostgreSQL (Production Recommended)
1. Install PostgreSQL adapter:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'portfolio_db',
           'USER': 'db_user',
           'PASSWORD': 'db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### MySQL
1. Install MySQL adapter:
   ```bash
   pip install mysqlclient
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'portfolio_db',
           'USER': 'db_user',
           'PASSWORD': 'db_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Django settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if not using SQLite)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=portfolio_db
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password

# Professional information
PERSONAL_NAME=Your Name
PERSONAL_EMAIL=your.email@domain.com
PROFESSIONAL_TITLE=Cybersecurity Analyst
GITHUB_USERNAME=your-github-username
TRYHACKME_PROFILE=your-tryhackme-profile
HACKTHEBOX_PROFILE=your-hackthebox-profile
```

## Security Considerations

1. Always set `DEBUG=False` in production
2. Use a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` properly
4. Use HTTPS in production
5. Set secure headers in your web server configuration
6. Regularly update dependencies
7. Implement proper database backups
8. Use environment variables for sensitive information

## SSL Configuration

To enable HTTPS, obtain an SSL certificate and update your Nginx configuration:

```
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # ... rest of your configuration
}
```

## Maintenance

### Regular Tasks
1. Update dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. Run database migrations:
   ```bash
   python manage.py migrate
   ```

3. Collect static files after updates:
   ```bash
   python manage.py collectstatic
   ```

4. Restart services:
   ```bash
   sudo systemctl restart portfolio
   sudo systemctl restart nginx
   ```

### Backup Strategy
1. Database backup:
   ```bash
   # For SQLite
   cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
   
   # For PostgreSQL
   pg_dump portfolio_db > portfolio_backup_$(date +%Y%m%d).sql
   ```

2. Media files backup:
   ```bash
   tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
   ```

3. Code backup:
   Use Git to track changes and push to a remote repository.

## Troubleshooting

### Common Issues

1. **Permission denied errors**:
   Ensure proper file permissions for the project directory.

2. **Static files not loading**:
   Check that `collectstatic` was run and Nginx configuration is correct.

3. **Database connection errors**:
   Verify database settings and that the database service is running.

4. **Import errors**:
   Check that all dependencies are installed in the virtual environment.

### Logs

Check the following log locations for issues:
- Django logs: Check console output or configure logging in settings.py
- Gunicorn logs: `/var/log/gunicorn/`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog` or `/var/log/messages`

## Monitoring

Implement monitoring for:
1. Application uptime
2. Response times
3. Error rates
4. Resource usage (CPU, memory, disk)
5. Security events

Tools like Prometheus, Grafana, or commercial solutions can be used for monitoring.

---
*Deployment guide last updated: September 2025*