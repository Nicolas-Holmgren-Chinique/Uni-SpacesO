"""
Home Models Module

This module contains model classes for the home app in the UniSpaces
social networking application. It defines database models for managing
dynamic content that appears on the homepage and base templates.

Key Features:
- Dynamic content management through database
- Content type categorization for different page sections
- Timestamp tracking for content creation
- Admin-friendly content management

Dependencies:
- Django ORM for database operations
- Model field types for content storage

Usage:
Models are used to store and retrieve content that populates
the homepage and base template sections of the application.
"""

# Import Django database functionality
from django.db import models

class HomeContent(models.Model):
    """
    Model for storing dynamic content used across the application
    
    This model allows administrators to manage text content that appears
    on various pages without requiring code changes. Content is categorized
    by type to allow for different sections and layouts.
    
    Fields:
        title: The heading or title for the content section
        description: The main text content (supports longer text)
        created_at: Automatic timestamp when content was created
        type: Category of content (home page vs base template)
    
    Content Types:
        - 'home': Content specific to the main homepage
        - 'base': Content that appears across multiple pages
    
    Use Cases:
        - Welcome messages and site descriptions
        - Feature announcements and updates
        - Terms of service or policy text
        - Promotional content and calls-to-action
    
    Future Enhancements:
        - Rich text editing support (HTML content)
        - Image attachments for visual content
        - Content scheduling (publish/expire dates)
        - Multi-language support
        - Content versioning and approval workflow
    """
    
    # Content type choices for categorization
    TITLE_CHOICE = [
        ('home', 'Home'),
        ('base', 'Base'),
    ]

    # Main title or heading for the content
    title = models.CharField(
        max_length=200,
        help_text="The title or heading for this content section"
    )
    
    # Main text content - supports longer descriptions
    description = models.TextField(
        help_text="The main text content for this section"
    )
    
    # Automatic timestamp for content creation tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this content was first created"
    )
    
    # Content categorization for different page sections
    type = models.CharField(
        max_length=10, 
        choices=TITLE_CHOICE,
        help_text="Where this content should appear (home page or base template)"
    )

    class Meta:
        """
        Meta configuration for HomeContent model
        """
        # Order content by creation date (newest first)
        ordering = ['-created_at']
        
        # Verbose names for Django admin interface
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        """
        String representation of the HomeContent model
        
        Returns:
            str: The title of the content for easy identification
        """
        return f"{self.title} ({self.get_type_display()})"
