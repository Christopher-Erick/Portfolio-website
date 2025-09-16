from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.conf import settings
from django.utils.cache import get_cache_key
from django.http import HttpRequest
from .models import ContactSubmission, Skill, Experience, Education, UserProfile, Certification, Achievement, Testimonial, SecurityEvent


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('cv_document', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


def clear_resume_cache():
    """Clear the resume cache when resume-related data is updated"""
    # Clear specific cache keys that might be used
    cache.delete('resume_data')
    # Clear any other potential cache keys
    cache.delete_many(['resume_view', 'skills_data', 'education_data', 'experience_data'])
    # Clear home page cache by using a more direct approach
    # Since we can't easily generate the exact cache key used by @cache_page,
    # we'll clear the entire cache for the home page path
    from django.core.cache import caches
    from django.conf import settings
    
    # Get the default cache
    cache_backend = caches[getattr(settings, 'CACHE_MIDDLEWARE_ALIAS', 'default')]
    
    # Clear cache entries (this is a simplified approach)
    try:
        # For development with locmem cache, this might work
        if hasattr(cache_backend, '_cache'):
            # Clear locmem cache
            cache_backend._cache.clear()
        elif hasattr(cache_backend, '_cache_client'):
            # For other cache backends, try to clear
            cache.clear()
    except:
        # Fallback: clear using cache.clear()
        cache.clear()

    # Also clear template fragment cache if used
    cache.delete(make_template_fragment_key('home_testimonials'))
    
    # Most reliable approach: Clear all cache (as a last resort)
    # cache.clear()  # Uncomment this if the above approaches don't work


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cv_filename', 'uploaded_at', 'download_link']
    list_filter = ['uploaded_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['uploaded_at', 'download_link']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()
    
    def download_link(self, obj):
        if obj.cv_document:
            return f'<a href="{obj.cv_document.url}" target="_blank">Download CV</a>'
        return 'No CV uploaded'
    download_link.allow_tags = True
    download_link.short_description = 'Download'


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'icon']
    list_filter = ['category']
    search_fields = ['name']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['start_date', 'end_date']
    search_fields = ['company', 'position']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['institution', 'degree', 'field_of_study']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'expiry_date', 'is_expired']
    list_filter = ['issue_date', 'expiry_date', 'issuing_organization']
    search_fields = ['name', 'issuing_organization', 'credential_id']
    fields = ['name', 'issuing_organization', 'issue_date', 'expiry_date', 'credential_id', 'credential_url', 'description', 'icon']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['order', 'is_active']
    fields = ['title', 'description', 'icon', 'technologies', 'order', 'is_active']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()
    
    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'position', 'short_content', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'company']
    search_fields = ['name', 'company', 'position', 'content']
    list_editable = ['order', 'is_active']
    fields = ['name', 'position', 'company', 'content', 'order', 'is_active']
    
    actions = ['clear_home_page_cache']
    
    def clear_home_page_cache(self, request, queryset):
        """Clear home page cache when testimonials are updated"""
        clear_resume_cache()
        self.message_user(request, "Home page cache cleared successfully.")
    clear_home_page_cache.short_description = "Clear home page cache"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_resume_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_resume_cache()
    
    def short_content(self, obj):
        return obj.short_content
    short_content.short_description = 'Testimonial Content'


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'severity', 'ip_address', 'username', 'created_at']
    list_filter = ['event_type', 'severity', 'created_at']
    search_fields = ['ip_address', 'username', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False  # Security events should only be created by the system
    
    def has_change_permission(self, request, obj=None):
        return False  # Security events should be immutable
    
    fieldsets = (
        ('Event Information', {
            'fields': ('event_type', 'severity', 'description', 'created_at')
        }),
        ('Request Details', {
            'fields': ('ip_address', 'username', 'path', 'method', 'user_agent')
        }),
    )