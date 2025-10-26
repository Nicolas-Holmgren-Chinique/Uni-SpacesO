#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unispaces.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def fix_superuser_password():
    print("=== Fixing Superuser Password ===")
    
    # Get the testadmin user
    user = User.objects.filter(username='testadmin').first()
    if user:
        print(f"Found user: {user.username}")
        
        # Set a known password
        user.set_password('admin123')
        user.save()
        print("Password reset to 'admin123'")
        
        # Test authentication
        auth_result = authenticate(username='testadmin', password='admin123')
        print(f"Authentication test: {'SUCCESS' if auth_result else 'FAILED'}")
        
        # Also test direct password check
        password_check = user.check_password('admin123')
        print(f"Direct password check: {'SUCCESS' if password_check else 'FAILED'}")
        
    else:
        print("testadmin user not found!")

if __name__ == "__main__":
    fix_superuser_password()
