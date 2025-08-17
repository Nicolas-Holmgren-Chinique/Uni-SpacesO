"""
Home Views Module

This module contains view functions for the home app in the UniSpaces
social networking application. It handles the main landing page
and content management functionality.

Key Features:
- Dynamic content loading from database
- Separate content types for different page sections
- Template rendering with context data

Dependencies:
- Django shortcuts for rendering
- HomeContent model for content management

Usage:
These views are mapped to URLs in home/urls.py and provide
the main entry point for users visiting the application.
"""

# Import Django core functionality
from django.shortcuts import render
from .models import HomeContent

def home(request):
    """
    Render the main homepage with dynamic content
    
    This view loads content from the database to populate the homepage.
    It retrieves different types of content to allow for flexible
    page management without code changes.
    
    Content Types:
    - 'home': Main homepage content and sections
    - 'base': Base template content that appears across pages
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered homepage template with content
        
    Template:
        home/home.html - Main homepage template
        
    Context Variables:
        content: QuerySet of home-specific content objects
        base_content: QuerySet of base template content objects
        
    Future Enhancements:
        - User-specific content based on authentication status
        - A/B testing for different homepage versions
        - Analytics tracking for homepage interactions
        - Featured communities or recent activity
    """
    # Load home-specific content from database
    content = HomeContent.objects.filter(type='home')
    
    # Load base template content that appears across multiple pages
    base_content = HomeContent.objects.filter(type='base') 
    
    # Render the homepage template with content
    return render(request, 'home/home.html', {
        'content': content, 
        'base_content': base_content
    })
