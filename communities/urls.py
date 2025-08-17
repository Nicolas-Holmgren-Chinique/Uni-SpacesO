"""
Communities URL Configuration

This module defines URL patterns for the communities app in the UniSpaces
social networking application. It maps URL patterns to view functions
that handle community-related functionality.

URL Patterns:
- community/create/ -> Community creation form and processing
- Additional patterns commented out for future implementation

Dependencies:
- Django URL routing system
- Community views from this app

Usage:
These URLs are included in the main project URL configuration
and handle routing for all community-related pages.
"""

# Import Django URL routing functionality
from django.urls import path
from . import views

# URL patterns for community functionality
urlpatterns = [
    # Community creation endpoint
    path('community/create/', views.create_community, name='create_community'),
    
    # Future community detail page (currently commented out)
    # This would show individual community pages with posts and member lists
    # path('community/<slug:slug>/', views.community_detail, name='community_detail')
    
    # Additional URL patterns could include:
    # - Community member management
    # - Community settings/editing
    # - Join/leave community functionality
    # - Community post creation and viewing
]
