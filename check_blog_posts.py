#!/usr/bin/env python
"""
Script to check blog posts and their authors
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from blog.models import BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()

def check_blog_posts():
    """Check all blog posts and their authors"""
    posts = BlogPost.objects.all()
    
    print(f"Found {posts.count()} blog posts:")
    print("=" * 50)
    
    for post in posts:
        author = post.author
        print(f"Title: {post.title}")
        print(f"Author username: {author.username}")
        print(f"Author first_name: '{author.first_name}'")
        print(f"Author last_name: '{author.last_name}'")
        print(f"Author full name: '{author.get_full_name()}'")
        print(f"Author email: {author.email}")
        print("-" * 30)

if __name__ == '__main__':
    check_blog_posts()