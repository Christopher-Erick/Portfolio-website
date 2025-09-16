from django.contrib import admin
from .models import BlogCategory, Tag, BlogPost, Comment, PostLike, PostView


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 'total_likes', 'total_dislikes', 'total_views', 'published_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['reading_time', 'created_at', 'updated_at', 'total_likes', 'total_dislikes', 'total_views']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('tags', 'status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('total_likes', 'total_dislikes', 'total_views')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Metadata', {
            'fields': ('reading_time', 'published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Mark selected comments as approved"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Mark selected comments as not approved"


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'is_like', 'ip_address', 'created_at']
    list_filter = ['is_like', 'created_at']
    search_fields = ['post__title', 'ip_address']


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['post__title', 'ip_address']