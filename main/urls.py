from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('resume/', views.resume, name='resume'),
    path('resume/download/', views.download_resume, name='download_resume'),
    path('contact/', views.contact, name='contact'),
    path('security-dashboard/', views.security_dashboard, name='security_dashboard'),
    path('health/', views.health_check, name='health_check'),  # Health check endpoint for Fly.io
]