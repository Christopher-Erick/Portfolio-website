from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, Category, Technology


def portfolio_list(request):
    """Portfolio listing page with filtering"""
    projects = Project.objects.filter(is_featured=True).select_related('category').prefetch_related('technologies')
    categories = Category.objects.all()
    technologies = Technology.objects.all()
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        projects = projects.filter(category__slug=category_filter)
    
    # Filter by technology
    tech_filter = request.GET.get('technology')
    if tech_filter:
        projects = projects.filter(technologies__name__icontains=tech_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 9)  # Show 9 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'technologies': technologies,
        'current_category': category_filter,
        'current_technology': tech_filter,
        'search_query': search_query,
    }
    
    return render(request, 'portfolio/portfolio_list.html', context)


def project_detail(request, slug):
    """Individual project detail page"""
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('technologies', 'features', 'images'),
        slug=slug
    )
    
    # Get related projects (same category, exclude current project)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id).select_related('category')[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'portfolio/project_detail.html', context)


def filter_projects(request):
    """AJAX endpoint for filtering projects"""
    category = request.GET.get('category', '')
    technology = request.GET.get('technology', '')
    search = request.GET.get('search', '')
    
    projects = Project.objects.filter(is_featured=True).select_related('category').prefetch_related('technologies')
    
    if category:
        projects = projects.filter(category__slug=category)
    
    if technology:
        projects = projects.filter(technologies__name__icontains=technology)
    
    if search:
        from django.db.models import Q
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(short_description__icontains=search)
        )
    
    project_data = []
    for project in projects:
        project_data.append({
            'title': project.title,
            'slug': project.slug,
            'short_description': project.short_description,
            'category': project.category.name,
            'technologies': [tech.name for tech in project.technologies.all()],
            'featured_image': project.featured_image.url if project.featured_image else '',
            'live_url': project.live_url,
            'github_url': project.github_url,
            'status': project.get_status_display(),
        })
    
    return JsonResponse({'projects': project_data})