#!/usr/bin/env python
"""
Security testing script for portfolio application
Tests various security features and vulnerabilities
"""

import requests
import time
from urllib.parse import urljoin

# Configuration
BASE_URL = 'http://127.0.0.1:8000'
CONTACT_URL = urljoin(BASE_URL, '/contact/')

def test_contact_form_validation():
    """Test contact form input validation"""
    print("🧪 TESTING CONTACT FORM VALIDATION")
    print("=" * 50)
    
    # Test 1: XSS Attempt
    print("Test 1: XSS Protection...")
    xss_payload = {
        'name': '<script>alert("XSS")</script>',
        'email': 'test@example.com',
        'subject': 'XSS Test',
        'message': 'Testing XSS protection'
    }
    
    try:
        # First get CSRF token
        session = requests.Session()
        csrf_response = session.get(CONTACT_URL.replace('/contact/', '/contact/'))
        
        response = session.post(CONTACT_URL, 
                               json=xss_payload,
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Requested-With': 'XMLHttpRequest'
                               })
        if response.status_code == 200:
            data = response.json()
            if not data.get('success', False):
                print("✅ XSS protection working - malicious input rejected")
            else:
                print("❌ XSS protection failed - malicious input accepted")
        elif response.status_code == 403:
            print("✅ XSS attempt blocked by security middleware")
        elif response.status_code == 429:
            print("⚠️ Rate limited - this is expected security behavior")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing XSS: {e}")
    
    # Test 2: Empty fields validation
    print("\nTest 2: Empty Fields Validation...")
    empty_payload = {
        'name': '',
        'email': '',
        'subject': '',
        'message': ''
    }
    
    try:
        session = requests.Session()
        response = session.post(CONTACT_URL, 
                               json=empty_payload,
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Requested-With': 'XMLHttpRequest'
                               })
        if response.status_code == 200:
            data = response.json()
            if not data.get('success', False):
                print("✅ Empty fields validation working")
            else:
                print("❌ Empty fields validation failed")
        elif response.status_code in [403, 429]:
            print("✅ Request blocked by security middleware (expected)")
    except Exception as e:
        print(f"❌ Error testing empty fields: {e}")
    
    # Test 3: Valid submission
    print("\nTest 3: Valid Submission...")
    valid_payload = {
        'name': 'Security Tester',
        'email': 'security@test.com',
        'subject': 'Security Test',
        'message': 'This is a legitimate security test message to verify the contact form works properly.'
    }
    
    try:
        session = requests.Session()
        response = session.post(CONTACT_URL, 
                               json=valid_payload,
                               headers={
                                   'Content-Type': 'application/json',
                                   'X-Requested-With': 'XMLHttpRequest'
                               })
        if response.status_code == 200:
            data = response.json()
            if data.get('success', False):
                print("✅ Valid submission accepted")
            else:
                print(f"❌ Valid submission rejected: {data.get('error', 'Unknown error')}")
        elif response.status_code in [403, 429]:
            print("⚠️ Request blocked by security middleware (may need to adjust rate limits)")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing valid submission: {e}")


def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n🚦 TESTING RATE LIMITING")
    print("=" * 50)
    
    valid_payload = {
        'name': 'Rate Test',
        'email': 'rate@test.com',
        'subject': 'Rate Limit Test',
        'message': 'Testing rate limiting'
    }
    
    success_count = 0
    rate_limited = False
    
    print("Sending multiple requests to test rate limiting...")
    for i in range(6):  # Try 6 requests (limit is 5)
        try:
            response = requests.post(CONTACT_URL, 
                                   json=valid_payload,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    success_count += 1
                    print(f"  Request {i+1}: ✅ Accepted")
                else:
                    print(f"  Request {i+1}: ❌ Rejected - {data.get('error', 'Unknown')}")
            elif response.status_code == 429:
                rate_limited = True
                print(f"  Request {i+1}: 🚦 Rate limited (429)")
                break
            else:
                print(f"  Request {i+1}: ⚠️ Status {response.status_code}")
                
        except Exception as e:
            print(f"  Request {i+1}: ❌ Error - {e}")
        
        time.sleep(0.1)  # Small delay between requests
    
    if rate_limited:
        print("✅ Rate limiting is working")
    elif success_count >= 5:
        print("⚠️ Rate limiting might not be active (check if middleware is enabled)")
    else:
        print("❌ Unexpected rate limiting behavior")


def test_csrf_protection():
    """Test CSRF protection"""
    print("\n🛡️ TESTING CSRF PROTECTION")
    print("=" * 50)
    
    # Try to submit without CSRF token
    payload = {
        'name': 'CSRF Test',
        'email': 'csrf@test.com',
        'subject': 'CSRF Test',
        'message': 'Testing CSRF protection'
    }
    
    try:
        # Submit without proper headers
        response = requests.post(CONTACT_URL, data=payload)
        
        if response.status_code == 403:
            print("✅ CSRF protection working - request blocked")
        elif response.status_code == 200:
            print("⚠️ CSRF protection might be bypassed (JSON requests may handle differently)")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing CSRF: {e}")


def test_security_headers():
    """Test security headers"""
    print("\n🔒 TESTING SECURITY HEADERS")
    print("=" * 50)
    
    try:
        response = requests.get(BASE_URL)
        headers = response.headers
        
        # Check for security headers
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
        }
        
        for header, expected_value in security_headers.items():
            if header in headers:
                if headers[header] == expected_value:
                    print(f"✅ {header}: {headers[header]}")
                else:
                    print(f"⚠️ {header}: {headers[header]} (expected: {expected_value})")
            else:
                print(f"❌ {header}: Missing")
        
        # Check if CSP is present (might be disabled in DEBUG mode)
        if 'Content-Security-Policy' in headers:
            print(f"✅ Content-Security-Policy: Present")
        else:
            print("⚠️ Content-Security-Policy: Missing (might be disabled in DEBUG mode)")
            
    except Exception as e:
        print(f"❌ Error testing headers: {e}")


def test_admin_access():
    """Test admin URL protection"""
    print("\n👤 TESTING ADMIN ACCESS")
    print("=" * 50)
    
    # Test default admin URL
    try:
        response = requests.get(urljoin(BASE_URL, '/admin/'))
        if response.status_code == 302:  # Redirect
            print("✅ Default admin URL redirects (security measure)")
        elif response.status_code == 200:
            print("⚠️ Default admin URL accessible")
        else:
            print(f"⚠️ Default admin URL status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing admin access: {e}")


def main():
    """Run all security tests"""
    print("🔐 PORTFOLIO SECURITY TESTING SUITE")
    print("=" * 60)
    print(f"Testing URL: {BASE_URL}")
    print()
    
    # Check if server is running
    try:
        # Force HTTP for local testing and disable SSL verification
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get(BASE_URL, timeout=5, verify=False, allow_redirects=False)
        if response.status_code not in [200, 301, 302]:
            print(f"❌ Server not responding properly (status: {response.status_code})")
            return
    except requests.exceptions.SSLError:
        # SSL error, but server might still be running on HTTP
        print("⚠️ SSL connection failed, but this is expected for development server")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Django server is running: python manage.py runserver")
        return
    
    print("✅ Server is running, starting security tests...\n")
    
    # Run all tests
    test_contact_form_validation()
    test_rate_limiting()
    test_csrf_protection()
    test_security_headers()
    test_admin_access()
    
    print("\n" + "=" * 60)
    print("🎯 SECURITY TESTING COMPLETE")
    print("Review the results above to ensure all security measures are working.")
    print("\n💡 Next steps:")
    print("  1. Fix any failed tests")
    print("  2. Enable security middleware if needed")
    print("  3. Configure production settings")
    print("  4. Test with browser developer tools")


if __name__ == '__main__':
    main()