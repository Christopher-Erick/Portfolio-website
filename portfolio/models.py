from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class or image URL')
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    
    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('development', 'In Development'),
        ('completed', 'Completed'),
        ('maintenance', 'Maintenance'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text='Brief description for project cards')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    technologies = models.ManyToManyField(Technology, related_name='projects')
    
    # Project details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Links
    live_url = models.URLField(blank=True, help_text='Live project URL')
    github_url = models.URLField(blank=True, help_text='GitHub repository URL')
    demo_url = models.URLField(blank=True, help_text='Demo or video URL')
    
    # Media
    featured_image = models.ImageField(upload_to='projects/', blank=True)
    gallery_images = models.TextField(blank=True, help_text='JSON array of image URLs')
    writeup_document = models.FileField(upload_to='projects/writeups/', blank=True, help_text='Project writeup or report (PDF, DOC, DOCX)')
    
    # SEO and metadata
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text='Order for displaying projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})
    
    @property
    def is_active(self):
        return self.status in ['development', 'completed', 'maintenance']


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return f'{self.project.title} - {self.title}'


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.project.title} - Image {self.order}'