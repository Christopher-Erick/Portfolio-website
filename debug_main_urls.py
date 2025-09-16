#!/usr/bin/env python
"""
Debug URL loading issue
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.urls import get_resolver

def debug_main_urls():
    """Debug main app URLs specifically"""
    print("🔍 DEBUGGING MAIN APP URLs")
    print("=" * 40)
    
    urlconf = get_resolver()
    
    # Find main app URLs
    for pattern in urlconf.url_patterns:
        if hasattr(pattern, 'url_patterns') and str(pattern.pattern) == '':
            print("Found main app URLs:")
            for sub_pattern in pattern.url_patterns:
                print(f"  ✅ {sub_pattern.pattern} -> {sub_pattern.callback}")
            break
    else:
        print("❌ Could not find main app URL patterns")

if __name__ == '__main__':
    debug_main_urls()