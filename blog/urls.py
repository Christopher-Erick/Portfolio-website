from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('search/', views.search_posts, name='search_posts'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/like/', views.post_like, name='post_like'),
]