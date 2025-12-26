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
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Community, Membership
from .forms import CommunityForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from .project_views import project_gallery, project_detail, global_launchpad

@login_required
@require_http_methods(["GET", "POST"])
def create_community(request):
    """
    Handle community creation with hierarchical structure support
    
    This view manages the creation of both super communities (parent communities)
    and sub-communities (child communities). The hierarchical system allows for
    organizational structure like Universities -> Departments -> Study Groups.
    
    Supports both regular form submission and AJAX requests for modal popup.
    
    Process Flow:
    1. User fills out community creation form
    2. System validates for duplicate community names
    3. System determines if creating super or sub community
    4. For super communities: Creates parent + initial sub-community
    5. For sub communities: Creates child under existing parent
    6. Automatically assigns creator as member of new community(ies)
    7. Returns success response (JSON for AJAX, redirect for regular form)
    
    Args:
        request: HTTP request object containing form data
        
    Returns:
        JsonResponse: For AJAX requests with success/error data
        HttpResponse: For regular requests - rendered form page or redirect
        
    Security:
        - Requires user authentication via @login_required decorator
        - Validates community name uniqueness within same parent
        - Automatic membership prevents orphaned communities
        
    Template:
        community/create.html - Community creation form interface (for non-AJAX)
    """
    if request.method == 'POST':
        # Process submitted form data
        form = CommunityForm(request.POST)
        
        # Check if this is an AJAX request
        is_ajax = (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 
                  request.content_type == 'application/json' or
                  'application/json' in request.headers.get('Accept', ''))
        
        if form.is_valid():
            # Extract community type from form
            ctype = form.cleaned_data['community_type']
            title = form.cleaned_data['title']
            
            try:
                if ctype == 'super':
                    # Check for duplicate super community names
                    if Community.objects.filter(title__iexact=title, parent=None).exists():
                        error_msg = f"A super community with the name '{title}' already exists."
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'errors': {'title': [error_msg]}
                            })
                        else:
                            form.add_error('title', error_msg)
                            return render(request, 'community/create.html', {'form': form})
                    
                    # Create the super community (parent level)
                    super_comm = Community.objects.create(
                        title=title,
                        description=form.cleaned_data['description'],
                        parent=None,  # No parent = top-level community
                        is_parent=True,  # Mark as parent community
                        # created_by=request.user  # Future enhancement
                    )
                    # Automatically make creator a member
                    Membership.objects.create(user=request.user, community=super_comm)

                    # Create the initial sub-community under the super community
                    sub_title = form.cleaned_data['sub_title']
                    sub_comm = Community.objects.create(
                        title=sub_title,
                        description=form.cleaned_data['sub_description'],
                        parent=super_comm,  # Link to parent community
                        is_parent=False,  # Mark as sub-community
                    )
                    # Make creator a member of sub-community too
                    Membership.objects.create(user=request.user, community=sub_comm)

                elif ctype == 'sub':
                    parent = form.cleaned_data['parent']
                    
                    # Check for duplicate sub-community names within the same parent
                    if Community.objects.filter(title__iexact=title, parent=parent).exists():
                        error_msg = f"A sub-community with the name '{title}' already exists in {parent.title}."
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'errors': {'title': [error_msg]}
                            })
                        else:
                            form.add_error('title', error_msg)
                            return render(request, 'community/create.html', {'form': form})
                    
                    # Create a sub-community under existing parent
                    sub_comm = Community.objects.create(
                        title=title,
                        description=form.cleaned_data['description'],
                        parent=parent,  # Link to selected parent
                        is_parent=False,  # Mark as sub-community
                        # created_by=request.user  # Future enhancement
                    )
                    # Automatically assign membership
                    Membership.objects.create(user=request.user, community=sub_comm)

                # Success response
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Community created successfully!'
                    })
                else:
                    return redirect('dashboard')
                    
            except Exception as e:
                # Handle any unexpected errors  
                error_msg = f"An unexpected error occurred: {str(e)}"
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'errors': {'__all__': [error_msg]}
                    })
                else:
                    form.add_error(None, error_msg)
        else:
            # Form validation failed
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        # Display empty form for GET requests
        form = CommunityForm()

    # Render the community creation template (for non-AJAX requests)
    return render(request, 'community/create.html', {'form': form})


@login_required
def community_dashboard(request, slug):
    """
    Sub-Community Dashboard View
    
    This view displays a dashboard for a specific super community,
    showing all its sub-communities as floating planets. When users
    click on a super community planet in the main dashboard, they
    are brought here to see the sub-communities within that super community.
    
    Args:
        request: HTTP request object
        slug: URL-friendly identifier for the super community
        
    Returns:
        HttpResponse: Rendered dashboard template with sub-community data
        
    Context:
        - parent_community: The super community being viewed
        - sub_communities: All sub-communities under this super community
        - planet_data: JSON data for visualizing sub-communities as planets
        - user_memberships: User's membership status in communities
    """
    # Get the parent community
    parent_community = get_object_or_404(Community, slug=slug, is_parent=True)
    
    # Check if user is a member of the parent community
    is_member = Membership.objects.filter(
        user=request.user, 
        community=parent_community
    ).exists()
    
    if not is_member:
        messages.error(request, "You must be a member of this community to view its dashboard.")
        return redirect('dashboard')
    
    # Get all sub-communities under this parent
    sub_communities = Community.objects.filter(parent=parent_community)
    
    # Get user's memberships for highlighting communities they belong to
    user_memberships = Membership.objects.filter(
        user=request.user,
        community__in=sub_communities
    ).values_list('community_id', flat=True)
    
    # Prepare planet data for JavaScript visualization
    planet_data = [
        {
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "color": c.color,
            "is_parent": c.is_parent,
            "is_member": c.id in user_memberships,
            "url": f"/communities/{c.slug}/"
        }
        for c in sub_communities
    ]
    
    context = {
        'parent_community': parent_community,
        'sub_communities': sub_communities,
        'planet_data': json.dumps(planet_data),
        'section': 'community_dashboard',
        'user_memberships': user_memberships,
    }
    
    return render(request, 'community/dashboard.html', context)


@login_required  
def community_detail(request, slug):
    """
    Individual Community Detail View
    
    This view displays the details of a specific community where users
    can collaborate, ask questions, share work, etc. This is where users
    land when they click on a sub-community planet.
    
    Args:
        request: HTTP request object
        slug: URL-friendly identifier for the community
        
    Returns:
        HttpResponse: Rendered community detail template
        
    Context:
        - community: The community being viewed
        - is_member: Whether current user is a member
        - can_join: Whether user can join this community
    """
    community = get_object_or_404(Community, slug=slug)
    
    # Check membership status
    is_member = Membership.objects.filter(
        user=request.user,
        community=community
    ).exists()
    
    # For now, anyone can join any community
    # In the future, you might add approval processes
    can_join = not is_member
    
    context = {
        'community': community,
        'is_member': is_member,
        'can_join': can_join,
        'section': 'community_detail',
    }
    
    return render(request, 'community/detail.html', context)
