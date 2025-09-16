from django.urls import path
from . import views
from .debug_views import debug_resume_data, test_skills_template

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('resume/', views.resume, name='resume'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('icon-test/', views.icon_test, name='icon_test'),
    path('security-dashboard/', views.security_dashboard, name='security_dashboard'),
    path('download-security-report/', views.download_security_report, name='download_security_report'),
    path('debug-resume-data/', debug_resume_data, name='debug_resume_data'),
    path('test-skills/', test_skills_template, name='test_skills'),
]