# 🧩 Portfolio Website Components Overview

## Project Structure

```
RESUME/
├── blog/                 # Blog application
├── main/                 # Main application
├── portfolio/            # Portfolio application
├── portfolio_site/       # Django project settings
├── static/               # Static assets (CSS, JS, Images)
├── templates/            # Base templates
├── logs/                 # Application logs
├── media/                # Uploaded media files
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## Core Applications

### 1. Main Application (`main/`)
The main application contains the core functionality of the portfolio website.

**Key Components:**
- **Views**: Home, About, Contact, Resume, Security Dashboard
- **Models**: UserProfile, ContactSubmission, Skill, Experience, Education, Certification, Achievement, Testimonial, SecurityEvent
- **Middleware**: SecurityHeadersMiddleware, RateLimitMiddleware, SecurityLoggingMiddleware, BlockSuspiciousRequestsMiddleware
- **Templates**: home.html, about.html, contact.html, resume.html, security_dashboard.html
- **Static Files**: Custom CSS and JavaScript

**Key Features:**
- Homepage with animated security arsenal
- Professional resume with skills and experience
- Contact form with spam protection
- Security dashboard for monitoring
- Responsive design with dark/light mode

### 2. Portfolio Application (`portfolio/`)
Manages the project portfolio section of the website.

**Key Components:**
- **Views**: Portfolio list, Project detail
- **Models**: Category, Technology, Project
- **Templates**: portfolio_list.html, project_detail.html

**Key Features:**
- Project showcase with filtering
- Technology tagging
- Project detail pages

### 3. Blog Application (`blog/`)
Handles the blog section for sharing cybersecurity knowledge.

**Key Components:**
- **Views**: Blog list, Post detail
- **Models**: Category, Tag, Post, Comment, Like, View
- **Templates**: blog_list.html, post_detail.html

**Key Features:**
- Blog post listing
- Individual post pages
- Like/dislike functionality
- Comment system
- Tag-based organization

## Static Assets

### CSS (`static/css/`)
- **style.css**: Main stylesheet with responsive design
- **components.css**: Component-specific styling
- **icons.css**: Icon styling

**Key Features:**
- Modern, tech-oriented design
- Dark/light mode support
- Responsive grid system
- Animation utilities
- Component styling

### JavaScript (`static/js/`)
- **main.js**: Core JavaScript functionality

**Key Features:**
- Theme toggle (dark/light mode)
- Mobile menu functionality
- Form validation and handling
- Animation triggers
- Portfolio filtering
- Blog search
- Smooth scrolling

### Images (`static/images/`)
- Profile images
- Project screenshots
- Icons and favicons
- Background elements

## Templates

### Base Template (`templates/base.html`)
- HTML document structure
- Navigation menu
- Footer
- Meta tags
- CSS/JavaScript inclusion
- Theme support

### Main Templates
1. **home.html** - Homepage with all sections
2. **about.html** - Professional background and philosophy
3. **resume.html** - Detailed resume with skills and experience
4. **contact.html** - Contact form and information
5. **security_dashboard.html** - Admin security metrics

### Portfolio Templates
1. **portfolio_list.html** - Project gallery
2. **project_detail.html** - Individual project view

### Blog Templates
1. **blog_list.html** - Post listing
2. **post_detail.html** - Individual post view

## Configuration Files

### Django Settings (`portfolio_site/settings.py`)
- Application configuration
- Security settings
- Database configuration
- Static file handling
- Email settings
- Cache configuration
- Custom context processors

### Environment Configuration (`.env`)
- Sensitive configuration data
- Database settings
- Email configuration
- Security keys
- Admin settings

### Requirements (`requirements.txt`)
- Django 5.2.6
- Pillow 11.1.0
- reportlab 4.4.3
- whitenoise 6.9.0

## Database Models

### Main App Models
- **UserProfile**: User profile information
- **ContactSubmission**: Contact form submissions
- **Skill**: Professional skills with proficiency levels
- **Experience**: Work experience timeline
- **Education**: Educational background
- **Certification**: Professional certifications
- **Achievement**: Key accomplishments
- **Testimonial**: Client/colleague testimonials
- **SecurityEvent**: Security-related events

### Portfolio App Models
- **Category**: Project categories
- **Technology**: Technologies used
- **Project**: Individual projects

### Blog App Models
- **Category**: Post categories
- **Tag**: Post tags
- **Post**: Blog posts
- **Comment**: Post comments
- **Like**: Post feedback
- **View**: Post view tracking

## URL Structure

### Main URLs
- `/` - Homepage
- `/about/` - About page
- `/contact/` - Contact page
- `/resume/` - Resume page
- `/download-resume/` - Resume PDF download
- `/security-dashboard/` - Admin security dashboard
- `/download-security-report/` - Security report download

### Portfolio URLs
- `/portfolio/` - Project listing
- `/portfolio/<slug>/` - Individual project

### Blog URLs
- `/blog/` - Post listing
- `/blog/<slug>/` - Individual post
- `/blog/category/<slug>/` - Category filtering
- `/blog/tag/<slug>/` - Tag filtering

## Security Components

### Middleware
- **SecurityHeadersMiddleware**: Adds security headers
- **RateLimitMiddleware**: Implements rate limiting
- **SecurityLoggingMiddleware**: Logs security events
- **BlockSuspiciousRequestsMiddleware**: Blocks malicious requests

### Security Models
- **SecurityEvent**: Tracks security-related activities

### Security Scripts
- **security_manager.py**: Security audit and monitoring
- **config.py**: Secure configuration loader

## Deployment Components

### Production Files
- **.env.example**: Environment configuration template
- **Procfile**: Deployment configuration
- **runtime.txt**: Python version specification
- **setup.sh**: Deployment setup script

### Documentation
- **README.md**: Project overview
- **DEPLOYMENT_GUIDE.md**: Deployment instructions
- **SECURITY.md**: Security implementation guide
- **PROJECT_SUMMARY.md**: Project summary
- **TECHNICAL_DOCUMENTATION.md**: Technical documentation

## Custom Features

### Security Arsenal
- Interactive tool cards with proficiency levels
- Animated progress bars
- Hover effects with descriptions
- Category-based organization

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Media queries for different screen sizes
- Touch-friendly navigation

### Dark/Light Mode
- Theme toggle functionality
- CSS variables for theme colors
- Local storage for preference saving
- System preference detection

### Animations
- Fade-in effects on scroll
- Slide-in animations
- Hover effects
- Typing animation for hero section

### Interactive Elements
- Portfolio filtering
- Blog search
- Contact form validation
- Like/dislike functionality
- Mobile menu toggle

---
*Component overview last updated: September 2025*