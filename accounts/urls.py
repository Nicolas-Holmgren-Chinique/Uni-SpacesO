"""
Accounts URL Configuration

This module defines URL patterns for user authentication and profile management
in the UniSpaces social networking application. It maps URL patterns to view
classes that handle user account functionality.

URL Patterns:
- login/ -> User login with custom styling
- signup/ -> User registration with extended profile creation
- logout/ -> User logout with custom redirect
- dashboard/ -> Main user dashboard with community visualization
- profile/ -> User profile viewing
- profile/edit/ -> Profile editing functionality
- profile/remove-picture/ -> Profile picture removal

Dependencies:
- Django authentication system
- Custom view classes from accounts.views
- Profile management functionality

Usage:
These URLs are included in the main project URL configuration
and handle routing for all user account related pages.
"""

# Import Django authentication views and URL routing
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    CustomLoginView, 
    DashboardView, 
    SignUpView, 
    CustomLogoutView, 
    EditProfileView, 
    ProfileView, 
    RemoveProfilePictureView
)

# URL patterns for account management
urlpatterns = [
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Main application dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Profile management URLs
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/remove-picture/', RemoveProfilePictureView.as_view(), name='remove_profile_picture'),
]

# Development notes preserved for reference
"""
Development Progress Notes:

User Authentication System:
- ✅ Login functionality with custom styling and space theme
- ✅ Signup with extended UserProfile creation
- ✅ Logout with proper session management
- ✅ Dashboard with community visualization canvas

Profile Management System:
- ✅ Profile viewing with astronaut helmet fallback
- ✅ Profile editing with image upload
- ✅ Profile picture removal functionality
- ✅ University and bio fields for academic networking

Next Potential Features:
- Password reset functionality
- Email verification for new accounts
- User settings page
- Privacy controls
- Account deletion
"""


