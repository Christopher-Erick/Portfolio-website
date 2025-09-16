from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('filter/', views.filter_projects, name='filter_projects'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
]