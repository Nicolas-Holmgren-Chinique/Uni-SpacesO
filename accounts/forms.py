"""
Django Forms for User Account Management

This module defines custom forms for user registration and profile management
in the UniSpaces social network platform. Forms handle user input validation,
data cleaning, and the creation/updating of user accounts and profiles.

Forms in this module:
- SignUpForm: Extended user registration with university field
- ProfileForm: Profile editing for bio, university, and profile picture

Django forms provide:
- Automatic HTML form generation
- Data validation and cleaning
- Security features (CSRF protection)
- Error handling and display
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class SignUpForm(UserCreationForm):
    """
    Extended User Registration Form
    
    This form extends Django's built-in UserCreationForm to include
    additional fields specific to the UniSpaces platform. It handles
    user registration and automatically creates an associated UserProfile
    with university information.
    
    Additional Fields:
        email: User's email address (required)
        university: User's university affiliation (required)
        
    Inherited Fields (from UserCreationForm):
        username: Unique username for the account
        password1: Password field
        password2: Password confirmation field
    
    Features:
        - Email validation and uniqueness checking
        - University field for academic affiliation
        - Automatic UserProfile creation upon successful registration
        - Built-in password validation and matching
    """
    
    # Email field - required for account creation
    email = forms.EmailField(
        required=True,
        help_text="Your email address will be used for account notifications."
    )
    
    # University field - required for academic context
    university = forms.CharField(
        max_length=100, 
        required=True,
        help_text="The university you attend or attended."
    )

    class Meta:
        """
        Meta configuration for the SignUpForm
        
        Defines which model to use and which fields to include
        in the form rendering and validation.
        """
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the user and create associated UserProfile
        
        This method extends the parent save() method to create
        a UserProfile instance with the university information
        when a new user is registered.
        
        Args:
            commit (bool): Whether to save to database immediately
            
        Returns:
            User: The created user instance
            
        Process:
            1. Create User instance (don't save yet if commit=False)
            2. Set email from cleaned form data
            3. Save User to database if commit=True
            4. Create associated UserProfile with university info
            5. Return the User instance
        """
        # Call parent save method but don't commit yet
        user = super().save(commit=False)
        
        # Set email from the cleaned form data
        user.email = self.cleaned_data['email']
        
        if commit:
            # Save the User instance to database
            user.save()
            
            # Create the related UserProfile with university info
            # This creates the 1:1 relationship between User and UserProfile
            UserProfile.objects.create(
                user=user, 
                university=self.cleaned_data['university']
            )
        return user


class ProfileForm(forms.ModelForm):
    """
    User Profile Editing Form
    
    This form allows users to edit their profile information including
    their profile picture, biographical information, and university
    affiliation. It uses ModelForm to automatically generate form
    fields based on the UserProfile model.
    
    Editable Fields:
        profile_picture: Image upload for user's profile photo
        bio: Text area for biographical information
        university: Text field for university affiliation
    
    Features:
        - Image upload with validation
        - Text area with character limit for bio
        - University field for academic affiliation
        - Automatic form validation based on model constraints
        - File handling for profile picture uploads
        
    Usage:
        Used in EditProfileView to provide form-based profile editing
        functionality. The form automatically handles file uploads,
        validation, and saving to the UserProfile model.
    """
    
    class Meta:
        """
        Meta configuration for ProfileForm
        
        Defines the model to use and which fields to include
        in the form. Django automatically generates appropriate
        form widgets based on the model field types.
        """
        model = UserProfile
        fields = ['profile_picture', 'bio', 'university']
        
        # Optional: Custom help text for form fields
        help_texts = {
            'profile_picture': 'Upload a profile picture (optional). If not provided, the default astronaut helmet will be used.',
            'bio': 'Tell others about yourself (max 500 characters).',
            'university': 'Your university or educational institution.',
        }
        
        # Optional: Custom labels for form fields  
        labels = {
            'profile_picture': 'Profile Picture',
            'bio': 'Biography',
            'university': 'University',
        }
        
        # Optional: Custom widgets for enhanced form rendering
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'university': forms.TextInput(attrs={
                'placeholder': 'e.g., University of California, Berkeley'
            }),
        }
