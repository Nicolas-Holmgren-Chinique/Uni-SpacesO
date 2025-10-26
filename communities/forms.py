"""
Communities Forms Module

This module contains form classes for community creation and management
in the UniSpaces social networking application. It provides a sophisticated
form system that supports hierarchical community creation with validation.

Key Features:
- Hierarchical community creation (super/sub communities)
- Dynamic form validation based on community type
- Bootstrap-styled form widgets
- Custom validation for parent-child relationships

Dependencies:
- Django forms framework
- Community model from this app

Usage:
Forms are used in views to collect user input for community creation
and provide proper validation and error handling.
"""

from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    """
    Form for creating both super communities and sub-communities
    
    This form handles the complex logic of creating hierarchical communities.
    It dynamically adjusts required fields based on the community type
    selected by the user.
    
    Community Types:
    - Super Community: Creates a parent community with an initial sub-community
    - Sub Community: Creates a child community under an existing parent
    
    Form Fields:
    - community_type: Radio buttons to select super or sub community
    - title: Name of the community being created
    - description: Detailed description of the community purpose
    - parent: Select dropdown for choosing parent (sub communities only)
    - sub_title: Name for initial sub-community (super communities only)
    - sub_description: Description for initial sub-community (super communities only)
    
    Validation:
    - Sub communities must have a parent selected
    - Super communities must include initial sub-community details
    - All fields have appropriate Bootstrap styling
    """
    
    # Community type selection - determines form behavior
    COMMUNITY_TYPE_CHOICES = [
        ('super', 'Super Community'),
        ('sub', 'Sub Community'),
    ]

    community_type = forms.ChoiceField(
        choices=COMMUNITY_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label='Community Type',
        help_text='Super communities are top-level (like Universities). Sub communities are nested (like Departments).'
    )

    # Fields used only when creating super communities with initial sub-community
    sub_title = forms.CharField(
        required=False,
        label='Initial Sub-Community Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter sub-community name'
        }),
        help_text='Every super community needs at least one sub-community to start'
    )
    
    sub_description = forms.CharField(
        required=False,
        label='Initial Sub-Community Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Describe the sub-community',
            'rows': 3
        }),
        help_text='Explain what this sub-community will be used for'
    )

    class Meta:
        """
        Meta configuration for CommunityForm
        """
        model = Community
        fields = ['title', 'description', 'parent']
        
        # Bootstrap styling for all form fields
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter community name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Describe the community',
                'rows': 4
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        # User-friendly field labels
        labels = {
            'title': 'Community Name',
            'description': 'Community Description',
            'parent': 'Parent Community',
        }
        
        # Help text for form fields
        help_texts = {
            'title': 'Choose a descriptive name for your community',
            'description': 'Explain the purpose and goals of this community',
            'parent': 'Select the parent community (only for sub-communities)',
        }

    def clean(self):
        """
        Custom validation for community creation form
        
        This method validates the form data based on the selected community type
        and ensures that all required fields are provided for each type.
        
        Validation Rules:
        - Sub communities must have a parent community selected
        - Super communities must include initial sub-community details
        - Form displays appropriate error messages for missing data
        
        Returns:
            dict: Cleaned form data after validation
            
        Raises:
            ValidationError: If required fields are missing for selected type
        """
        cleaned_data = super().clean()
        ctype = cleaned_data.get("community_type")

        # Validation for sub-community creation
        if ctype == "sub" and not cleaned_data.get("parent"):
            self.add_error("parent", "You must choose a parent community for a sub-community.")

        # Validation for super community creation
        if ctype == "super":
            # For super communities, clear the parent field since it's not needed
            cleaned_data['parent'] = None
            
            if not cleaned_data.get("sub_title"):
                self.add_error("sub_title", "Super communities must include an initial sub-community.")
            if not cleaned_data.get("sub_description"):
                self.add_error("sub_description", "Please describe your initial sub-community.")
        else:
            # For sub communities, clear the sub-community fields since they're not needed
            cleaned_data['sub_title'] = ''
            cleaned_data['sub_description'] = ''

        return cleaned_data
