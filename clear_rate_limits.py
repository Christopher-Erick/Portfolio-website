#!/usr/bin/env python
"""
Script to check and clear rate limits for a specific IP address
"""
import os
import django
from django.core.cache import cache

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

def check_rate_limits(ip_address=None):
    """Check current rate limits"""
    print("🔍 Checking Rate Limits")
    print("=" * 25)
    
    # If no IP provided, show all rate limit keys
    if not ip_address:
        print("⚠️  Showing all rate limit keys (this may be a lot):")
        try:
            # This is a simplified approach - in production, you might want to be more specific
            print("💡 To check specific IP, provide an IP address as argument")
        except Exception as e:
            print(f"❌ Error checking cache: {e}")
        return
    
    # Check specific IP
    rate_limit_keys = [
        f'rate_limit_contact_{ip_address}',
        f'rate_limit_admin_{ip_address}',
        f'rate_limit_general_{ip_address}'
    ]
    
    for key in rate_limit_keys:
        try:
            current = cache.get(key, 0)
            print(f"  {key}: {current} requests")
        except Exception as e:
            print(f"  {key}: Error checking - {e}")

def clear_rate_limits(ip_address=None):
    """Clear rate limits"""
    print("🧹 Clearing Rate Limits")
    print("=" * 25)
    
    if ip_address:
        rate_limit_keys = [
            f'rate_limit_contact_{ip_address}',
            f'rate_limit_admin_{ip_address}',
            f'rate_limit_general_{ip_address}'
        ]
        
        for key in rate_limit_keys:
            try:
                cache.delete(key)
                print(f"✅ Cleared {key}")
            except Exception as e:
                print(f"❌ Error clearing {key}: {e}")
    else:
        # Clear all rate limits (use with caution)
        try:
            cache.clear()
            print("✅ All cache cleared (including rate limits)")
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")

def get_client_ip():
    """Get client IP - in real usage, this would come from request"""
    import socket
    try:
        # This is a simplified approach for demonstration
        # In real usage, you'd get this from the request object
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        ip_address = sys.argv[2] if len(sys.argv) > 2 else None
        
        if command == 'check':
            check_rate_limits(ip_address)
        elif command == 'clear':
            clear_rate_limits(ip_address)
        else:
            print("Usage: python clear_rate_limits.py [check|clear] [ip_address]")
            print("Examples:")
            print("  python clear_rate_limits.py check 192.168.1.100")
            print("  python clear_rate_limits.py clear 192.168.1.100")
            print("  python clear_rate_limits.py clear  # Clear all cache")
    else:
        print("🔧 Rate Limit Management Script")
        print("=" * 30)
        print("This script helps manage rate limits in your Django application.")
        print()
        print("Commands:")
        print("  check [ip]    - Check current rate limits for an IP")
        print("  clear [ip]    - Clear rate limits for an IP")
        print("  clear         - Clear all cache (including rate limits)")
        print()
        print("Note: In a deployed environment like Render, you would run these")
        print("commands through the Render console/shell.")