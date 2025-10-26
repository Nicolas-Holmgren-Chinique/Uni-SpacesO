#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unispaces.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_missing_profiles():
    print("=== Creating Missing UserProfiles ===")
    
    users_without_profiles = []
    
    for user in User.objects.all():
        try:
            profile = user.userprofile
            print(f"✓ {user.username} already has profile")
        except UserProfile.DoesNotExist:
            users_without_profiles.append(user)
    
    print(f"\nFound {len(users_without_profiles)} users without profiles")
    
    for user in users_without_profiles:
        profile = UserProfile.objects.create(
            user=user,
            university="Default University" if not user.is_superuser else "Admin University"
        )
        print(f"✓ Created profile for {user.username}")
    
    print(f"\n=== Verification ===")
    for user in User.objects.all():
        try:
            profile = user.userprofile
            print(f"✓ {user.username}: {profile.university}")
        except UserProfile.DoesNotExist:
            print(f"✗ {user.username}: No profile!")

if __name__ == "__main__":
    create_missing_profiles()
