from django.http import JsonResponse
from django.shortcuts import render
from .models import Skill, Education, Certification, Achievement, Experience

def debug_resume_data(request):
    """Debug view to check what data is being passed to the resume template"""
    # Get all data as the resume view does
    education_items = Education.objects.all()
    certifications = Certification.objects.all()
    achievements = Achievement.objects.filter(is_active=True)
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    
    # Apply the same categorization logic
    skills_by_category = {}
    category_mapping = {
        'skill': 'Skills',
        'tools': 'Tools',
        'soft': 'Special Skills',
    }
    
    for skill in skills:
        mapped_category = category_mapping.get(skill.category, skill.category)
        if mapped_category not in skills_by_category:
            skills_by_category[mapped_category] = []
        skills_by_category[mapped_category].append({
            'name': skill.name,
            'category': skill.category,
            'mapped_category': mapped_category,
            'proficiency': skill.proficiency
        })
    
    # Return JSON response with the data
    data = {
        'education_count': education_items.count(),
        'certifications_count': certifications.count(),
        'achievements_count': achievements.count(),
        'skills_count': skills.count(),
        'experiences_count': experiences.count(),
        'skills_by_category': skills_by_category,
        'categories': list(skills_by_category.keys())
    }
    
    return JsonResponse(data)

def test_skills_template(request):
    """Test view to render just the skills section"""
    # Get all skills
    skills = Skill.objects.all()
    
    # Apply the same categorization logic as in the resume view
    skills_by_category = {}
    category_mapping = {
        'skill': 'Skills',
        'tools': 'Tools',
        'soft': 'Special Skills',
    }
    
    for skill in skills:
        mapped_category = category_mapping.get(skill.category, skill.category)
        if mapped_category not in skills_by_category:
            skills_by_category[mapped_category] = []
        skills_by_category[mapped_category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category
    }
    
    return render(request, 'main/test_skills.html', context)