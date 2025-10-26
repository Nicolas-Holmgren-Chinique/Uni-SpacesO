#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unispaces.settings')
django.setup()

from django.urls import reverse, resolve
from django.conf import settings

def debug_urls():
    print("=== URL Debugging ===")
    
    # Test URL reversing
    try:
        login_url = reverse('login')
        print(f"Login URL: {login_url}")
        
        dashboard_url = reverse('dashboard')
        print(f"Dashboard URL: {dashboard_url}")
        
        signup_url = reverse('signup')
        print(f"Signup URL: {signup_url}")
    except Exception as e:
        print(f"Error reversing URLs: {e}")
    
    # Test URL resolving
    try:
        login_resolver = resolve('/accounts/login/')
        print(f"Login view: {login_resolver.func}")
        print(f"Login view name: {login_resolver.view_name}")
        
        dashboard_resolver = resolve('/accounts/dashboard/')
        print(f"Dashboard view: {dashboard_resolver.func}")
        print(f"Dashboard view name: {dashboard_resolver.view_name}")
        
    except Exception as e:
        print(f"Error resolving URLs: {e}")
    
    # Check settings
    print(f"\nLOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Not set')}")
    print(f"LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Not set')}")

if __name__ == "__main__":
    debug_urls()
