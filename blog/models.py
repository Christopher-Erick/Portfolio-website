from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Content
    excerpt = models.TextField(max_length=300, help_text='Brief description for post previews')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Reading time (calculated automatically)
    reading_time = models.IntegerField(default=0, help_text='Estimated reading time in minutes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Calculate reading time (assuming 200 words per minute)
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def total_likes(self):
        return self.post_likes.filter(is_like=True).count()
    
    @property
    def total_dislikes(self):
        return self.post_likes.filter(is_like=False).count()
    
    @property
    def total_views(self):
        return self.post_views.count()


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'


class PostLike(models.Model):
    """Model to track likes/dislikes on blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='post_likes')
    # Store IP address to prevent multiple likes from same user/IP
    ip_address = models.GenericIPAddressField()
    # True for like, False for dislike
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'ip_address')  # One vote per IP per post
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} on {self.post.title}"


class PostView(models.Model):
    """Model to track views on blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='post_views')
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'ip_address')  # One view per IP per post
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"View on {self.post.title}"