from django.shortcuts import render, get_object_or_404
from .models import Community
from .project_models import Project

def project_gallery(request, community_slug):
    community = get_object_or_404(Community, slug=community_slug)
    projects = community.projects.all().order_by('-created_at')
    
    context = {
        'community': community,
        'projects': projects,
    }
    return render(request, 'communities/project_gallery.html', context)

def project_detail(request, community_slug, project_slug):
    community = get_object_or_404(Community, slug=community_slug)
    project = get_object_or_404(Project, slug=project_slug, community=community)
    
    context = {
        'community': community,
        'project': project,
    }
    return render(request, 'communities/project_detail.html', context)

def global_launchpad(request):
    projects = Project.objects.all().order_by('-created_at')
    context = {
        'projects': projects,
    }
    return render(request, 'communities/global_launchpad.html', context)
