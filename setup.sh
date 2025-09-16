# Django Portfolio Setup Script

# This script helps you set up the Django portfolio website

# 1. First, ensure you have Python 3.8+ installed
echo "Setting up Django Portfolio Website..."

# 2. Install required packages globally (or use virtual environment)
pip install django==5.2.6 pillow reportlab

# 3. Navigate to the project directory
cd /path/to/your/portfolio_site

# 4. Run migrations to set up the database
python manage.py makemigrations main
python manage.py makemigrations portfolio  
python manage.py makemigrations blog
python manage.py migrate

# 5. Create a superuser for admin access
python manage.py createsuperuser

# 6. Collect static files (for production)
python manage.py collectstatic --noinput

# 7. Run the development server
python manage.py runserver

echo "Portfolio website should now be running at http://127.0.0.1:8000"
echo "Admin panel available at http://127.0.0.1:8000/admin"