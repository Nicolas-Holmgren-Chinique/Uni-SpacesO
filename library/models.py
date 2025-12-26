from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Textbook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='textbooks')
    description = models.TextField(blank=True)
    cover_image_url = models.URLField(blank=True, help_text="URL to cover image")
    open_access_url = models.URLField(help_text="Link to the free PDF or web view")
    isbn = models.CharField(max_length=13, blank=True)
    provider = models.CharField(max_length=100, default="OpenStax", help_text="Source (e.g. OpenStax, Project Gutenberg)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class StudyMaterial(models.Model):
    """User-uploaded notes and study aids"""
    MATERIAL_TYPES = [
        ('notes', 'Class Notes'),
        ('summary', 'Chapter Summary'),
        ('cheatsheet', 'Cheat Sheet'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='study_materials/')
    description = models.TextField(blank=True)
    downloads = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"
