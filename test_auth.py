#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unispaces.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

def test_authentication():
    print("=== Authentication Test ===")
    
    # Check authentication backends
    print(f"Authentication backends: {getattr(settings, 'AUTHENTICATION_BACKENDS', 'Default')}")
    
    # Get all users
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    for user in users:
        print(f"User: {user.username}, Email: {user.email}, Superuser: {user.is_superuser}, Active: {user.is_active}")
    
    # Test superuser authentication
    superuser = User.objects.filter(username='testadmin').first()
    if superuser:
        print(f"\nTesting superuser: {superuser.username}")
        
        # Try direct password check
        password_check = superuser.check_password('admin123')
        print(f"  Direct password check 'admin123': {'SUCCESS' if password_check else 'FAILED'}")
        
        # Try authentication
        auth_result = authenticate(username='testadmin', password='admin123')
        status = "SUCCESS" if auth_result else "FAILED"
        print(f"  Django authenticate 'admin123': {status}")
        
        if not auth_result:
            print("  Authentication failed - checking user details...")
            print(f"  User active: {superuser.is_active}")
            print(f"  Password set: {bool(superuser.password)}")
            print(f"  Password hash: {superuser.password[:20]}...")
    else:
        print("No testadmin superuser found!")

if __name__ == "__main__":
    test_authentication()
