# Cybersecurity Professional Portfolio

A comprehensive Django-based portfolio website for showcasing cybersecurity expertise, projects, and professional experience.

## ⚠️ Important Notice

If you've deployed this application and it's missing personal information or projects, please see [FIX_DEPLOYMENT.md](FIX_DEPLOYMENT.md) for instructions on how to populate your database with the necessary data.

## Project Overview

This portfolio website is designed for cybersecurity professionals to showcase their skills, projects, and experience. It features a modern, responsive design with dark/light mode support and interactive elements.

## Features

- **Professional Portfolio**: Display skills, experience, education, and certifications
- **Project Showcase**: Highlight cybersecurity projects with detailed descriptions
- **Blog Section**: Share knowledge through technical blog posts
- **Security Dashboard**: Monitor website security metrics and events
- **Responsive Design**: Works on all device sizes
- **Dark/Light Mode**: Toggle between color schemes
- **Contact Form**: Allow visitors to get in touch

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development) or PostgreSQL (production)
- **Security**: Custom middleware, rate limiting, event logging

## Installation

### Standard Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd RESUME
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Visit `http://127.0.0.1:8000` in your browser

### Docker Installation (Recommended for Production)

For a containerized deployment, see [DOCKER_README.md](file:///c:/Users/CHRISTOPHER/Desktop/project/RESUME/DOCKER_README.md) for detailed instructions.

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