"""
Home App URL Configuration

This module defines URL patterns for the home app in the UniSpaces
social networking application. It handles the main landing page
and any home-related functionality.

URL Patterns:
- '' (root) -> Home page view

Dependencies:
- Django URL routing system
- Home views from this app

Usage:
This URL configuration is included in the main project URLs
and handles the application's homepage routing.
"""

# Import Django URL routing functionality
from django.urls import path
from .views import home

# URL patterns for home functionality
urlpatterns = [
    # Root URL - application homepage
    path('', home, name='home'),
    
    # Additional home-related URLs could include:
    # - About page
    # - Contact page
    # - Landing page for different user types
    # - Application features overview
]