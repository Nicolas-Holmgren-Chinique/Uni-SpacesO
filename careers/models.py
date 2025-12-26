from django.db import models
from django.contrib.auth.models import User

class Internship(models.Model):
    """
    Internship Opportunity (Mission Control)
    """
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    application_link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    
    # Tags/Skills could be added here too
    
    def __str__(self):
        return f"{self.title} at {self.company}"
