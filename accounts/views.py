"""
Django Views for User Account Management

This module contains all the view classes and functions for handling
user authentication, registration, profile management, and the main
dashboard functionality for the UniSpaces social network platform.

Views handle the business logic between models (data) and templates (presentation).
They process HTTP requests and return HTTP responses.

Main Features:
- User authentication (login/logout)
- User registration
- User dashboard with space-themed community visualization  
- Profile viewing and editing
- Profile picture management

Dependencies:
- Django's built-in authentication system
- Community model for displaying user's communities
- UserProfile model for extended user information
"""

# Standard library imports
import json

# Django core imports
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404

# Local app imports
from communities.models import Community
from .models import UserProfile
from .forms import ProfileForm, SignUpForm

"""
Authentication Views
"""

class CustomLoginView(LoginView):
    """
    Custom Login View extending Django's built-in LoginView
    
    This view handles user authentication and login functionality.
    It uses Django's built-in AuthenticationForm for security and
    validation, then redirects authenticated users to their dashboard.
    
    Attributes:
        template_name: Path to the login template
        redirect_authenticated_user: If True, already logged-in users 
                                   are redirected instead of seeing login form
        authentication_form: The form class used for authentication
    
    Methods:
        get_success_url(): Determines where to redirect after successful login
    """
    template_name = 'accounts/login.html'  # Path to your login template
    redirect_authenticated_user = True  # Redirect if user is already authenticated
    authentication_form = AuthenticationForm  # Use Django's built-in AuthenticationForm

    def get_form(self, form_class=None):
        """Override to add CSS classes to form fields"""
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        return form

    def form_invalid(self, form):
        """Handle invalid form submission - add debugging"""
        print(f"Login form errors: {form.errors}")
        print(f"Form cleaned data: {getattr(form, 'cleaned_data', 'No cleaned data')}")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """Handle valid form submission - add debugging"""
        print(f"Login successful for user: {form.get_user()}")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Determine redirect URL after successful login
        
        Returns:
            str: URL to redirect to after login (dashboard)
        """
        return reverse_lazy('dashboard')  # Redirect to the dashboard after login


class SignUpView(CreateView):
    """
    User Registration View with Auto-Login
    
    This view handles new user registration using a custom SignUpForm
    that includes email and university fields. It automatically logs 
    users in after successful registration and creates their UserProfile, 
    then redirects them directly to their dashboard.
    
    Attributes:
        form_class: Custom SignUpForm with email and university fields
        template_name: Path to the signup template
        success_url: Where to redirect after successful registration (dashboard)
    
    Methods:
        form_valid(): Called when form submission is valid - creates profile and logs user in
    """
    form_class = SignUpForm  # Use custom form with email and university
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')  # Redirect to dashboard instead of login

    def form_invalid(self, form):
        """Handle invalid form submission - add debugging"""
        print(f"Signup form errors: {form.errors}")
        print(f"Form data: {form.data}")
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        Handle valid form submission - create user, profile, and auto-login
        
        Args:
            form: The validated SignUpForm with email and university
            
        Returns:
            HttpResponseRedirect: Redirect to dashboard with user logged in
        """
        print(f"Signup form valid - creating user: {form.cleaned_data['username']}")
        
        # Save the user (this also creates the UserProfile via the form's save method)
        response = super().form_valid(form)
        
        # Get the newly created user
        user = self.object
        
        # Log the user in automatically
        login(self.request, user)
        
        # Add success message
        messages.success(self.request, f'Welcome to UniSpaces, {user.username}! Your account has been created successfully.')
        
        print(f"User {user.username} registered and logged in. Redirecting to dashboard.")
        return response


"""
Dashboard Views
"""

@login_required 
def dashboard(request):
    """
    Function-based Dashboard View (Alternative Implementation)
    
    This is an alternative implementation of the dashboard using a 
    function-based view instead of a class-based view. It demonstrates
    how to manually handle the community data preparation for the
    space-themed visualization.
    
    Args:
        request: HttpRequest object containing request data
        
    Returns:
        HttpResponse: Rendered dashboard template with context data
        
    Context Data:
        section: Identifies current page section
        planet_data: JSON string containing community data for canvas visualization
    """
    # Get parent communities that the user is a member of
    user_memberships = request.user.membership_set.all()
    user_community_ids = [membership.community.id for membership in user_memberships]
    parent_communities = Community.objects.filter(
        id__in=user_community_ids,
        is_parent=True
    )

    # Prepare community data for JavaScript canvas visualization
    # Each community becomes a "planet" in the space-themed interface
    planet_data = json.dumps([
        {
            "name": c.title,           # Community name displayed on planet
            "slug": c.slug,            # URL-friendly community identifier  
            "color": c.color,          # Planet color for visualization
            "is_parent": c.is_parent,  # Whether this is a parent community
            "url": f"/communities/{c.slug}/"  # URL to community page
        }
        for c in parent_communities  # Only include parent communities in main dashboard
    ])

    # Render the dashboard template with community data
    return render(
        request,
        'accounts/dashboard.html',
        {
            'section': 'dashboard',    # Used for navigation highlighting
            'planet_data': planet_data # JSON data for JavaScript visualization
        }
    )


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Class-based Dashboard View (Primary Implementation)
    
    This is the main dashboard view that displays the user's space-themed
    interface with floating community "planets". It requires user authentication
    and provides context data for both the user's profile and their communities.
    
    Attributes:
        template_name: Path to the dashboard template
    
    Features:
        - Displays user's communities as floating planets in a space canvas
        - Shows user profile information in dropdown menu
        - Provides navigation to community pages
        - Ensures user has a profile (creates one if needed)
    """
    template_name = 'accounts/dashboard.html'  # Path to your dashboard template
    
    def get_context_data(self, **kwargs):
        """
        Prepare context data for the dashboard template
        
        This method gathers all the data needed to render the dashboard,
        including user profile information and community data for the
        space visualization.
        
        Args:
            **kwargs: Additional keyword arguments from URL
            
        Returns:
            dict: Context dictionary containing all template data
        """
        context = super().get_context_data(**kwargs)
        
        # Ensure user has a profile - create one if it doesn't exist
        # get_or_create returns (object, created) tuple
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        
        # Get user's super communities only for main dashboard visualization
        # Main dashboard should only show parent communities (super communities)
        user_super_communities = Community.objects.filter(
            members__user=self.request.user,
            parent=None  # Only parent communities (super communities)
        ).distinct()
        
        # Get all super communities (parent=None) for modal dropdown
        super_communities = Community.objects.filter(parent=None)
        
        # Convert community data to JSON for JavaScript canvas rendering
        # Each community becomes a "planet" in the space interface
        # Main dashboard shows only super communities - clicking navigates to sub-dashboard
        planet_data = [
            {
                "id": c.id,                 # Community database ID
                "title": c.title,           # Community name shown on planet
                "slug": c.slug,             # URL-safe community identifier  
                "color": c.color,           # Color for planet visualization
                "is_parent": c.is_parent,   # Whether this is a parent community
                "parent_id": c.parent.id if c.parent else None,  # Parent community ID
                "url": f"/communities/{c.slug}/dashboard/"  # Link to sub-community dashboard
            }
            for c in user_super_communities
        ]
        
        # Add dashboard-specific context
        context.update({
            'section': 'dashboard',           # For navigation highlighting
            'planet_data': json.dumps(planet_data),  # Community data for JavaScript
            'super_communities': super_communities,   # For modal dropdown
            'user_communities': user_super_communities      # User's super communities for sidebar
        })
        
        return context
"""
Authentication & Logout Views
"""

class CustomLogoutView(LoginRequiredMixin, TemplateView):
    """
    Custom Logout View
    
    This view handles user logout functionality. It requires the user
    to be logged in (LoginRequiredMixin), logs them out, and redirects
    them to the login page.
    
    Attributes:
        template_name: Path to logout template (not used due to redirect)
    
    Methods:
        get(): Handles GET requests by logging out and redirecting
    """
    template_name = 'logout.html'  # Path to your logout template

    def get(self, request, *args, **kwargs):
        """
        Handle logout request
        
        Args:
            request: HttpRequest object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponseRedirect: Redirect to login page
        """
        logout(request)
        return redirect('login')  # Redirect to the login page after logout
    

"""
Profile Management Views

These views handle user profile viewing, editing, and profile picture management.
They provide functionality for users to customize their profiles and manage
their personal information within the UniSpaces platform.
"""

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User Profile Display View
    
    This view displays a user's profile information including their profile
    picture, bio, university, and other personal details. It can display
    either the current user's profile or another user's profile based on
    the username in the URL.
    
    Features:
        - Display user's profile information
        - Show profile picture or default astronaut helmet
        - Distinguish between own profile and other users' profiles
        - Automatic profile creation if none exists
    """
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        """
        Prepare context data for profile display
        
        This method determines which user's profile to display and
        gathers all necessary information for the template.
        
        Args:
            **kwargs: URL parameters, may include 'username'
            
        Returns:
            dict: Context dictionary with profile and user data
        """
        context = super().get_context_data(**kwargs)
        username = kwargs.get('username')
        
        # Determine which user's profile to display
        if username:
            # Display specific user's profile (from URL parameter)
            user = get_object_or_404(User, username=username)
        else:
            # Display current user's profile
            user = self.request.user
            
        # Ensure the user has a profile - create if doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Prepare context data for template
        context.update({
            'profile': profile,
            'user': user,
            'is_own_profile': self.request.user == user  # Flag for edit permissions
        })
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Profile Editing View
    
    This view allows users to edit their profile information including
    their profile picture, bio, and university affiliation. It uses
    Django's UpdateView for handling form processing and validation.
    
    Features:
        - Edit profile picture, bio, and university
        - Form validation and error handling
        - Success message after profile update
        - Automatic profile creation if none exists
    """
    model = UserProfile
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile_view')
    
    def get_object(self, queryset=None):
        """
        Get the UserProfile object to edit
        
        This method ensures that the current user's profile is loaded
        for editing, creating one if it doesn't exist.
        
        Args:
            queryset: Optional queryset (not used here)
            
        Returns:
            UserProfile: The user's profile object
        """
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        """
        Handle successful form submission
        
        This method is called when the form is successfully validated.
        It saves the profile and displays a success message to the user.
        
        Args:
            form: The validated ProfileForm
            
        Returns:
            HttpResponseRedirect: Redirect to success_url
        """
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

class RemoveProfilePictureView(LoginRequiredMixin, View):
    """
    Profile Picture Removal View
    
    This view handles the removal of a user's profile picture.
    It deletes the current profile picture file and resets the
    profile to use the default astronaut helmet image.
    
    Features:
        - Remove current profile picture file from storage
        - Reset profile picture field to None (triggers default image)
        - Success message confirmation
        - Handle both POST and GET requests (redirect GET to profile)
    """
    
    def post(self, request, *args, **kwargs):
        """
        Handle profile picture removal (POST request)
        
        This method processes the actual removal of the profile picture.
        It finds the user's profile, deletes the old picture file,
        and resets the profile picture field.
        
        Args:
            request: HttpRequest object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponseRedirect: Redirect to profile view
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.profile_picture:
            # Delete the actual image file from storage
            profile.delete_old_picture()
            # Reset the profile picture field to None
            profile.profile_picture = None
            profile.save()
            # Inform user of successful removal
            messages.success(request, 'Profile picture removed. Default astronaut helmet restored!')
        return redirect('profile_view')
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests (redirect to profile)
        
        GET requests to this view are redirected to the profile page
        since picture removal should only happen via POST for security.
        
        Args:
            request: HttpRequest object
            *args: Additional positional arguments  
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponseRedirect: Redirect to profile view
        """
        return redirect('profile_view')

"""
Context Processor for Global Template Access

This function provides global access to user profile data across all templates.
Context processors run for every request and add data to the template context
automatically, making it available without explicitly passing it in each view.
"""

def profile_context(request):
    """
    Add user profile to all templates globally
    
    This context processor ensures that user profile information is
    available in all templates without needing to explicitly pass it
    in each view. This is particularly useful for displaying profile
    pictures in navigation bars or headers.
    
    Args:
        request: HttpRequest object containing user information
        
    Returns:
        dict: Context dictionary with user_profile data
        
    Usage:
        Add 'accounts.views.profile_context' to TEMPLATES['OPTIONS']['context_processors']
        in settings.py to enable global access to user_profile in all templates.
        
        In templates: {{ user_profile.profile_picture.url }}
    """
    if request.user.is_authenticated:
        # Get or create profile for authenticated users
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return {'user_profile': profile}
    return {}  # Return empty dict for anonymous users