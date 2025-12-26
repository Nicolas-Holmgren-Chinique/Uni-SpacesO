from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    """Skills tagged on projects and user profiles"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    Student Project Showcase (The Launchpad)
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='projects')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    collaborators = models.ManyToManyField(User, related_name='collaborations', blank=True)
    
    # Rich Details
    poster_image = models.ImageField(upload_to='project_posters/', blank=True, null=True)
    abstract = models.TextField(help_text="Short summary of the project")
    description = models.TextField(help_text="Full project details")
    
    # Links
    repo_url = models.URLField(blank=True, help_text="Link to GitHub/GitLab repo")
    demo_url = models.URLField(blank=True, help_text="Link to live demo")
    
    # Skills
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)
    
    # Metrics
    upvotes = models.ManyToManyField(User, related_name='upvoted_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
