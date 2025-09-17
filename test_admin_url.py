#!/usr/bin/env python
"""
Test script to verify admin URL accessibility
"""
import requests
import os
from urllib.parse import urljoin

def test_admin_urls():
    """Test different admin URLs"""
    base_url = "https://christopher-erick-otieno-portfolio.onrender.com"
    
    # List of possible admin URLs to test
    admin_urls = [
        "/secure-admin-path-12345/",
        "/secure-admin-ceo789/",
        "/admin/",
        "/secure-admin-path-12345",
        "/secure-admin-ceo789",
        "/admin"
    ]
    
    print("🔍 Testing Admin URL Accessibility")
    print("=" * 35)
    
    for url_path in admin_urls:
        full_url = urljoin(base_url, url_path)
        try:
            response = requests.get(full_url, timeout=10)
            status = response.status_code
            if status == 200:
                print(f"✅ {full_url} - Status: {status} (SUCCESS)")
            elif status == 404:
                print(f"❌ {full_url} - Status: {status} (NOT FOUND)")
            elif status == 403:
                print(f"🔒 {full_url} - Status: {status} (FORBIDDEN - Admin panel likely here)")
            else:
                print(f"❓ {full_url} - Status: {status}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  {full_url} - Error: {str(e)}")
    
    print(f"\n📝 Note: A 403 status might indicate the admin panel is there but requires authentication")

if __name__ == '__main__':
    test_admin_urls()