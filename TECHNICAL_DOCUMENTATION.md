# Technical Documentation

## Project Architecture

This Django project follows a modular architecture with three main applications:
1. `main` - Core website functionality
2. `portfolio` - Project showcase
3. `blog` - Content management

## Main Application Components

### Views (`main/views.py`)

#### Home View
- Renders the homepage with security arsenal
- Handles contact form submissions
- Implements spam detection
- Rate limiting for form submissions

#### Resume View
- Displays professional resume
- Organizes skills by category
- Shows experience timeline

#### About View
- Presents professional background
- Displays cybersecurity philosophy

#### Contact View
- Renders contact form
- Processes form submissions
- Validates input data
- Implements rate limiting

#### Security Dashboard View
- Displays security metrics
- Shows recent security events
- Requires staff access

#### Download Views
- Resume PDF generation
- Security report generation

### Models (`main/models.py`)

#### UserProfile
Stores personal information:
- Name
- Email
- Professional title
- Social profiles
- Security metrics

#### ContactSubmission
Records contact form submissions:
- Name, email, subject, message
- Submission timestamp
- IP address tracking

#### Skill
Professional skills with proficiency levels:
- Name
- Category (Tools, Skills, Special Skills)
- Proficiency percentage

#### Experience
Professional experience details:
- Position, company
- Dates
- Description
- Technologies used

#### Education
Educational background:
- Degree, institution
- Dates
- Field of study

#### Certification
Professional certifications:
- Name, issuing organization
- Issue and expiry dates

#### Achievement
Key accomplishments:
- Title, description
- Associated technologies

#### Testimonial
Client/colleague testimonials:
- Name, role, company
- Content
- Rating

#### SecurityEvent
Security-related events:
- Event type (login, admin access, etc.)
- IP address
- Description
- Severity level

## Portfolio Application

### Models (`portfolio/models.py`)

#### Category
Project categories:
- Name
- Description

#### Technology
Technologies used:
- Name
- Icon

#### Project
Individual projects:
- Title, slug
- Description
- Technologies
- Links
- Featured status

### Views (`portfolio/views.py`)

#### Portfolio List
- Displays all projects
- Category filtering
- Search functionality

#### Project Detail
- Detailed project view
- Technology tags
- Related projects

## Blog Application

### Models (`blog/models.py`)

#### Category
Post categories:
- Name
- Description

#### Tag
Post tags:
- Name

#### Post
Blog posts:
- Title, slug
- Content
- Author
- Publication status
- Featured image
- Like/dislike tracking

#### Comment
Post comments:
- Author information
- Content
- Approval status

#### Like
Post feedback:
- User session
- Like/dislike status

#### View
Post view tracking:
- User session
- Timestamp

### Views (`blog/views.py`)

#### Blog List
- Paginated post listing
- Category filtering

#### Post Detail
- Full post content
- Like/dislike functionality
- Related posts
- View counting

## Templates

### Base Template (`templates/base.html`)
- HTML document structure
- Navigation menu
- Footer
- Meta tags
- CSS/JavaScript inclusion
- Theme support

### Main Templates
1. `home.html` - Homepage with all sections
2. `about.html` - Professional background
3. `resume.html` - Detailed resume
4. `contact.html` - Contact form and information
5. `security_dashboard.html` - Admin security metrics

### Portfolio Templates
1. `portfolio_list.html` - Project gallery
2. `project_detail.html` - Individual project view

### Blog Templates
1. `blog_list.html` - Post listing
2. `post_detail.html` - Individual post view

## Static Files

### CSS (`static/css/style.css`)
- Responsive grid system
- Component styling
- Animation utilities
- Dark/light theme variables
- Form styling
- Navigation and footer

### JavaScript (`static/js/main.js`)
- Theme management
- Mobile menu toggle
- Form validation
- Animation triggers
- Like/dislike functionality
- Security dashboard interactions

## Security Implementation

### Custom Middleware (`main/middleware.py`)
- Request rate limiting
- Suspicious activity detection
- Security event logging
- IP blocking for malicious requests

### Security Features
- Form spam detection
- Rate limiting for contact submissions
- Admin access logging
- Security event monitoring
- Threat level assessment

## Settings (`portfolio_site/settings.py`)

### Key Configurations
- Security middleware
- Static file handling
- Email settings
- Cache configuration
- Custom context processors
- Professional information variables

### Environment Variables
- DEBUG mode
- SECRET_KEY
- ALLOWED_HOSTS
- Email configuration

## URL Configuration

### Main URLs (`portfolio_site/urls.py`)
- Main app URLs
- Portfolio app URLs
- Blog app URLs
- Admin URLs
- Static file serving

### App URLs
Each app has its own `urls.py` defining:
- Page routes
- API endpoints
- Detail views

## Database Design

### Relationships
- UserProfile (one-to-one with User)
- Skills linked to UserProfile
- Experience linked to UserProfile
- Education linked to UserProfile
- Certifications linked to UserProfile
- Achievements linked to UserProfile
- Testimonials linked to UserProfile
- Projects linked to Categories and Technologies
- Posts linked to Categories and Tags
- Comments linked to Posts
- Likes linked to Posts
- Views linked to Posts

### Indexes
- Slug fields for URL generation
- Published dates for sorting
- Category relationships
- Tag relationships

## Performance Considerations

### Caching
- Template fragment caching
- Queryset caching
- Static file caching

### Optimization
- Database query optimization
- Image optimization
- Lazy loading for images
- Efficient CSS/JS delivery

## Deployment

### Production Settings
- DEBUG = False
- ALLOWED_HOSTS configuration
- Static file serving
- Database configuration
- Email backend setup

### Security Headers
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

## Custom Management Commands

### Data Population
- Skill creation
- Project import
- Blog post generation
- User profile setup

### Maintenance
- Security event cleanup
- View count aggregation
- Database optimization

## Testing

### Unit Tests
- Model validation
- View rendering
- Form processing
- Security middleware

### Integration Tests
- User flow testing
- Contact form submission
- Blog post interaction
- Portfolio navigation

## Future Enhancements

### Planned Features
- User authentication system
- Portfolio project submission
- Blog comment system
- Advanced analytics
- API endpoints
- Admin interface customization

### Performance Improvements
- Database indexing
- Query optimization
- Asset compression
- CDN integration

---
*Documentation last updated: September 2025*