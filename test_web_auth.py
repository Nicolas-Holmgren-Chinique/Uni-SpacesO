#!/usr/bin/env python
import os
import django
import requests

def test_web_authentication():
    """Test the actual web login/signup forms"""
    
    base_url = "http://localhost:8000"
    session = requests.Session()
    
    print("=== Testing Web Authentication ===\n")
    
    # Test 1: Get login page
    print("1. Testing login page access...")
    try:
        response = session.get(f"{base_url}/accounts/login/")
        print(f"   Login page status: {response.status_code}")
        
        # Check if we get the form
        if "csrf" in response.text.lower():
            print("   ✓ CSRF token found in login form")
        else:
            print("   ✗ CSRF token missing in login form")
            
    except Exception as e:
        print(f"   ✗ Error accessing login page: {e}")
    
    # Test 2: Get signup page  
    print("\n2. Testing signup page access...")
    try:
        response = session.get(f"{base_url}/accounts/signup/")
        print(f"   Signup page status: {response.status_code}")
        
        # Check if we get the form
        if "csrf" in response.text.lower():
            print("   ✓ CSRF token found in signup form")
        else:
            print("   ✗ CSRF token missing in signup form")
            
    except Exception as e:
        print(f"   ✗ Error accessing signup page: {e}")
    
    # Test 3: Test existing user login
    print("\n3. Testing login submission...")
    try:
        # Get CSRF token first
        response = session.get(f"{base_url}/accounts/login/")
        csrf_token = None
        
        # Extract CSRF token (basic extraction)
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                csrf_token = line.split('value="')[1].split('"')[0]
                break
        
        if csrf_token:
            print(f"   ✓ CSRF token extracted: {csrf_token[:10]}...")
            
            # Submit login form
            login_data = {
                'username': 'testadmin',
                'password': 'admin123',
                'csrfmiddlewaretoken': csrf_token
            }
            
            response = session.post(f"{base_url}/accounts/login/", data=login_data)
            print(f"   Login submission status: {response.status_code}")
            print(f"   Redirect URL: {response.url}")
            
            # Check if redirected to dashboard
            if 'dashboard' in response.url:
                print("   ✓ Login successful - redirected to dashboard")
            else:
                print("   ✗ Login failed - not redirected to dashboard")
                print(f"   Final URL: {response.url}")
        else:
            print("   ✗ Could not extract CSRF token")
            
    except Exception as e:
        print(f"   ✗ Error during login test: {e}")

if __name__ == "__main__":
    test_web_authentication()
