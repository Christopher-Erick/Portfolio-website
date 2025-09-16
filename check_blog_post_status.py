#!/usr/bin/env python
"""
Script to check blog post status and publication dates
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
    """Check all blog posts status and publication info"""
    posts = BlogPost.objects.all().order_by('-created_at')
    
    print(f"Found {posts.count()} blog posts:")
    print("=" * 60)
    
    for post in posts:
        author = post.author
        print(f"Title: {post.title}")
        print(f"Status: {post.status}")
        print(f"Published at: {post.published_at}")
        print(f"Is published: {post.is_published}")
        print(f"Author: {author.get_full_name()}")
        print("-" * 40)

if __name__ == '__main__':
    check_blog_posts()