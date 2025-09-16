from django.contrib import admin
from .models import Category, Technology, Project, ProjectFeature, ProjectImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'created_at']
    list_filter = ['category', 'status', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    inlines = [ProjectFeatureInline, ProjectImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'category')
        }),
        ('Technologies & Status', {
            'fields': ('technologies', 'status', 'start_date', 'end_date')
        }),
        ('Links', {
            'fields': ('live_url', 'github_url', 'demo_url')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images', 'writeup_document')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )