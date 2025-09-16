from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import BlogPost, BlogCategory, Tag, PostLike, PostView


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def blog_list(request):
    """Blog listing page with filtering and search"""
    posts = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    categories = BlogCategory.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    
    # Filter by tag
    tag_filter = request.GET.get('tag')
    if tag_filter:
        posts = posts.filter(tags__slug=tag_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Featured posts
    featured_posts = BlogPost.objects.filter(status='published', is_featured=True)[:3]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'featured_posts': featured_posts,
        'current_category': category_filter,
        'current_tag': tag_filter,
        'search_query': search_query,
    }
    
    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(
        BlogPost.objects.select_related('category', 'author').prefetch_related('tags', 'comments'),
        slug=slug,
        status='published'
    )
    
    # Track view (only count unique IPs)
    client_ip = get_client_ip(request)
    PostView.objects.get_or_create(
        post=post,
        ip_address=client_ip
    )
    
    # Get related posts (same category or tags, exclude current post)
    related_posts = BlogPost.objects.filter(
        Q(category=post.category) | Q(tags__in=post.tags.all()),
        status='published'
    ).exclude(id=post.id).distinct().select_related('category')[:3]
    
    # Handle comment submission
    if request.method == 'POST':
        from .forms import CommentForm
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return JsonResponse({'success': True, 'message': 'Thank you for your comment! It will be reviewed before being published.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)


@require_POST
@csrf_exempt
def post_like(request, slug):
    """Handle post like/dislike"""
    try:
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        client_ip = get_client_ip(request)
        
        # Parse JSON data
        data = json.loads(request.body)
        is_like = data.get('is_like', True)
        
        # Create or update like/dislike
        post_like, created = PostLike.objects.get_or_create(
            post=post,
            ip_address=client_ip,
            defaults={'is_like': is_like}
        )
        
        if not created:
            # If already exists, update the value
            if post_like.is_like != is_like:
                post_like.is_like = is_like
                post_like.save()
                message = "Updated your feedback!"
            else:
                # If same value, remove it
                post_like.delete()
                message = "Removed your feedback!"
        else:
            message = "Thank you for your feedback!"
        
        # Return updated counts
        return JsonResponse({
            'success': True,
            'message': message,
            'likes': post.total_likes,  # This will get the updated count
            'dislikes': post.total_dislikes  # This will get the updated count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })


def search_posts(request):
    """AJAX endpoint for searching blog posts"""
    query = request.GET.get('q', '')
    
    if len(query) < 3:
        return JsonResponse({'results': []})
    
    posts = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(excerpt__icontains=query) |
        Q(content__icontains=query),
        status='published'
    ).select_related('category')[:5]
    
    results = []
    for post in posts:
        results.append({
            'title': post.title,
            'slug': post.slug,
            'excerpt': post.excerpt,
            'category': post.category.name,
            'published_at': post.published_at.strftime('%B %d, %Y') if post.published_at else '',
            'url': post.get_absolute_url(),
        })
    
    return JsonResponse({'results': results})