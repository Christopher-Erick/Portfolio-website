from portfolio.models import Project

def check_projects():
    print("Total projects:", Project.objects.count())
    projects = Project.objects.all()
    for p in projects:
        print(f"Project: {p.title}")
        print(f"  Featured Image: {bool(p.featured_image)} ({p.featured_image})")
        print(f"  Writeup: {bool(p.writeup_document)} ({p.writeup_document})")
        print()

if __name__ == "__main__":
    import os
    import sys
    import django
    from django.conf import settings
    
    # Add the project directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
    django.setup()
    
    check_projects()