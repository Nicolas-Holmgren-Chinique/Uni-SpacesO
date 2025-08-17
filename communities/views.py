"""
Communities Views Module

This module contains view functions for community management functionality
in the UniSpaces social networking application. It handles community creation,
post management, and community interaction features.

Key Features:
- Community creation with hierarchical structure (super/sub communities)
- Automatic membership assignment upon creation
- Form-based community management
- User authentication requirements

Dependencies:
- Django shortcuts for rendering and redirects
- Authentication decorators for security
- Community models and forms

Usage:
These views are mapped to URLs in communities/urls.py and handle
the business logic for community-related user interactions.
"""

# Previous implementation for reference - included more comprehensive post functionality
# This commented section shows a more feature-complete community system with posts
# 
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Community, Post, Membership
# from .forms import CommunityForm, PostForm

# @login_required
# def create_community(request):
#     """
#     Handle community creation with automatic membership
#     """
#     if request.method == 'POST':
#         form = CommunityForm(request.POST)
#         if form.is_valid():
#             community = form.save(commit=False)
#             community.created_by = request.user
#             community.save()

#             # Automatically make creator a member of their community
#             Membership.objects.create(user=request.user, community=community)

#             return redirect('community_detail', title=community.title)
#     else:
#         form = CommunityForm()

#     return render(request, 'community/create.html', {'form': form})


# @login_required
# def community_detail(request, title):
#     """
#     Display community details with post creation functionality
#     """
#     community = get_object_or_404(Community, title=title)
#     posts = Post.objects.filter(community=community).order_by('-created_at')
#     is_member = Membership.objects.filter(user=request.user, community=community).exists()

#     if request.method == 'POST':
#         if not is_member:
#             return redirect('join_community', title=title)  # Optional gatekeeping

#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.community = community
#             post.author = request.user
#             post.save()
#             return redirect('community_detail', title=community.title)
#     else:
#         form = PostForm()

#     return render(request, 'community/detail.html', {
#         'community': community,
#         'posts': posts,
#         'form': form,
#         'is_member': is_member
#     })


# Import Django core functionality
from django.shortcuts import render, redirect
from .models import Community, Membership
from .forms import CommunityForm
from django.contrib.auth.decorators import login_required

@login_required
def create_community(request):
    """
    Handle community creation with hierarchical structure support
    
    This view manages the creation of both super communities (parent communities)
    and sub-communities (child communities). The hierarchical system allows for
    organizational structure like Universities -> Departments -> Study Groups.
    
    Process Flow:
    1. User fills out community creation form
    2. System determines if creating super or sub community
    3. For super communities: Creates parent + initial sub-community
    4. For sub communities: Creates child under existing parent
    5. Automatically assigns creator as member of new community(ies)
    6. Redirects to dashboard to view new community
    
    Args:
        request: HTTP request object containing form data
        
    Returns:
        HttpResponse: Rendered form page or redirect to dashboard
        
    Security:
        - Requires user authentication via @login_required decorator
        - Automatic membership prevents orphaned communities
        
    Template:
        community/create.html - Community creation form interface
    """
    if request.method == 'POST':
        # Process submitted form data
        form = CommunityForm(request.POST)
        if form.is_valid():
            # Extract community type from form
            ctype = form.cleaned_data['community_type']

            if ctype == 'super':
                # Create the super community (parent level)
                super_comm = Community.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    parent=None,  # No parent = top-level community
                    # created_by=request.user  # Future enhancement
                )
                # Automatically make creator a member
                Membership.objects.create(user=request.user, community=super_comm)

                # Create the initial sub-community under the super community
                sub_comm = Community.objects.create(
                    title=form.cleaned_data['sub_title'],
                    description=form.cleaned_data['sub_description'],
                    parent=super_comm,  # Link to parent community
                )
                # Make creator a member of sub-community too
                Membership.objects.create(user=request.user, community=sub_comm)

                return redirect('dashboard')

            elif ctype == 'sub':
                # Create a sub-community under existing parent
                sub_comm = Community.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    parent=form.cleaned_data['parent'],  # Link to selected parent
                    # created_by=request.user  # Future enhancement
                )
                # Automatically assign membership
                Membership.objects.create(user=request.user, community=sub_comm)

                return redirect('dashboard')
    else:
        # Display empty form for GET requests
        form = CommunityForm()

    # Render the community creation template
    return render(request, 'community/create.html', {'form': form})
