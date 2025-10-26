#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unispaces.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import UserProfile

def setup_test_users():
    print("=== Setting Up Test Users ===")
    
    # Fix all existing superuser passwords
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        user.set_password('admin123')  # Set consistent password
        user.save()
        print(f"Fixed password for superuser: {user.username}")
    
    # Create a test regular user
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'testuser@test.com',
            'is_active': True,
            'is_superuser': False,
            'is_staff': False
        }
    )
    
    if created:
        test_user.set_password('testpass')
        test_user.save()
        print(f"Created new regular user: {test_user.username}")
        
        # Create UserProfile
        UserProfile.objects.get_or_create(
            user=test_user,
            defaults={'university': 'Test University'}
        )
        print(f"Created UserProfile for: {test_user.username}")
    else:
        test_user.set_password('testpass')
        test_user.save()
        print(f"Updated password for existing user: {test_user.username}")
    
    # Test all users
    print("\n=== Testing All Users ===")
    
    # Test superusers
    for user in superusers:
        auth_result = authenticate(username=user.username, password='admin123')
        status = "SUCCESS" if auth_result else "FAILED"
        print(f"Superuser {user.username}: {status}")
    
    # Test regular user
    auth_result = authenticate(username='testuser', password='testpass')
    status = "SUCCESS" if auth_result else "FAILED"
    print(f"Regular user testuser: {status}")
    
    print("\n=== Login Credentials ===")
    print("Superusers: username/admin123")
    for user in superusers:
        print(f"  - {user.username}/admin123")
    print("Regular user: testuser/testpass")

if __name__ == "__main__":
    setup_test_users()
