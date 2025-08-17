"""
Django Models for User Account Management

This module defines the data models for extending Django's built-in User model
with additional profile information for the UniSpaces social network platform.

The main purpose is to store extra user information like university affiliation,
profile pictures, and biographical information that isn't included in Django's
default User model.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class UserProfile(models.Model):
    """
    Extended User Profile Model
    
    This model extends Django's built-in User model with additional fields
    specific to the UniSpaces platform. It uses a OneToOneField to create
    a 1:1 relationship with the User model, meaning each User has exactly
    one UserProfile.
    
    Fields:
        user: OneToOneField linking to Django's User model
        university: CharField for storing the user's university name
        profile_picture: ImageField for storing user's profile photo
        bio: TextField for user's biographical information
    
    The relationship allows us to access profile data via user.profile
    and user data via profile.user
    """

    # OneToOneField creates a 1:1 relationship with Django's User model
    # CASCADE means if the User is deleted, this profile is also deleted
    # default=1 is a temporary value for migration purposes
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    
    # University field - optional, can be blank or null
    university = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        help_text="The university this user attends or attended"
    )
    
    # Profile picture field - uploads to 'profile_pictures/' directory
    # Optional field, can be blank or null for default image
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text="User's profile picture - if not provided, default astronaut helmet is used"
    )
    
    # Bio field - for longer text descriptions
    # Limited to 500 characters to prevent extremely long bios
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="User's biographical information or personal description"
    )
    


    def __str__(self):
        """
        String representation of the UserProfile model
        
        Returns the username of the associated User object.
        This is useful for Django admin and debugging.
        """
        return self.user.username
    

    def get_profile_picture_url(self):
        """
        Get the URL for the user's profile picture
        
        Returns:
            str: URL to the profile picture if it exists, 
                 otherwise returns path to default image
        
        This method provides a safe way to get the profile picture URL
        without causing errors if the image doesn't exist.
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default_profile_picture.png'
    
    def delete_old_profile_picture(self):
        """
        Delete the old profile picture file from storage
        
        This method removes the actual image file from the filesystem
        when a user changes their profile picture or removes it entirely.
        This prevents orphaned files from accumulating on the server.
        
        Should be called before setting a new profile picture or
        when removing a profile picture entirely.
        """
        if self.profile_picture:
            if os.path.exists(self.profile_picture.path):
                os.remove(self.profile_picture.path)

    """
    Model Design Notes:
    
    User Profile model that extends the default User model with additional fields.
    This model includes fields for university affiliation, profile picture, and bio.
    
    Why we extend rather than replace Django's User model:
    - Django's User model provides authentication, permissions, and admin integration
    - We only need to add extra fields, not replace core functionality
    - This approach is recommended by Django documentation
    
    Fields NOT included here (they're in Django's User model):
    - username: User's unique identifier
    - email: User's email address  
    - password: Hashed password for authentication
    - first_name, last_name: User's name fields
    - is_active, is_staff, is_superuser: Permission flags
    - date_joined, last_login: Timestamp fields
    
    These can be accessed via the relationship: user_profile.user.username, etc.
    """

    # The commented out fields below are examples of what NOT to include
    # since they're already part of Django's User model:
    # username = models.CharField(max_length=150, unique=True)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=128)  # Store hashed password


"""
Signal Handlers (Currently Disabled)

The code below shows how to automatically create a UserProfile 
when a User is created using Django signals. This is currently 
commented out but could be enabled if needed.

Signals automatically trigger when certain database events occur,
like creating or saving a model instance.
"""

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """
#     Automatically create a UserProfile when a new User is created
#     
#     This signal handler listens for the post_save signal from the User model.
#     When a new User is created (created=True), it automatically creates
#     a corresponding UserProfile instance.
#     """
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     """
#     Automatically save the UserProfile when the User is saved
#     
#     This ensures that changes to the User model trigger saving
#     of the associated UserProfile if it exists.
#     """
#     instance.userprofile.save()