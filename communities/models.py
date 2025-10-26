"""
Django Models for Community Management

This module defines the data models for the     # Color for space-themed visualization
    color = models.CharField(
        max_length=50, 
        default=generate_random_color,
        help_text="HSL color for the community planet in space visualization"
    ),ity system in the UniSpaces
social network platform. Communities are the core organizational units where
users can gather around shared academic interests, subjects, or topics.

The system supports hierarchical communities with parent-child relationships,
allowing for organized subject matter (e.g., "Mathematics" as parent with 
"Calculus" and "Algebra" as children).

Models in this module:
- Community: Main community model with hierarchical support
- Membership: Many-to-many relationship between users and communities  
- Post: Content posted within communities

Key Features:
- Hierarchical community structure (parent-child relationships)
- Automatic slug generation for URL-friendly community names
- Random color generation for space-themed visualization
- Membership tracking with join timestamps
- Community posts and discussions
"""

import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

CARTOON_COLOR_PALETTE = (
    # Punchy warms
    "hsl(12, 92%, 62%)",   # vibrant coral
    "hsl(28, 92%, 64%)",   # orange sherbet
    "hsl(332, 88%, 70%)",  # playful pink
    # Bold cools
    "hsl(210, 84%, 56%)",  # electric blue
    "hsl(190, 82%, 66%)",  # aqua splash
    "hsl(162, 74%, 58%)",  # tropical teal
    # Friendly greens & yellows
    "hsl(132, 67%, 60%)",  # lime zest
    "hsl(48, 92%, 66%)",   # sunny gold
    # Moody accents
    "hsl(282, 72%, 68%)",  # dreamy violet
    "hsl(352, 78%, 62%)",  # ruby red
)


def generate_random_color():
    """Return a playful HSL color suited for cartoon planets."""
    return random.choice(CARTOON_COLOR_PALETTE)

class Community(models.Model):
    """
    Community Model for Organizing Users Around Shared Interests
    
    This model represents a community where users can gather to discuss
    topics, share content, and collaborate. Communities can be hierarchical,
    with parent communities containing subcommunities for better organization.
    
    For example:
    - "Mathematics" (parent) → "Calculus", "Algebra", "Statistics" (children)
    - "Computer Science" (parent) → "Algorithms", "Web Development" (children)
    
    Fields:
        title: Human-readable name of the community
        slug: URL-friendly version of the title (auto-generated)
        color: HSL color for space visualization (auto-generated)
        description: Detailed description of the community's purpose
        is_parent: Boolean indicating if this is a top-level community
        parent: Foreign key to parent community (if this is a subcommunity)
        created_at: Timestamp of community creation
        updated_at: Timestamp of last community update
    
    Relationships:
        - Self-referential: Communities can have parent-child relationships
        - Many-to-many with Users through Membership model
        - One-to-many with Posts
    """
    
    # Community title - must be unique across all communities
    title = models.CharField(
        max_length=100, 
        unique=True,
        help_text="The name of the community (e.g., 'Calculus', 'Computer Science')"
    )
    
    # URL-friendly slug - auto-generated from title
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        blank=True,
        help_text="URL-friendly version of the title (auto-generated)"
    )
    
    # Color for space-themed visualization
    color = models.CharField(
        max_length=50, 
        default=generate_random_color,
        help_text="HSL color for the community planet in space visualization"
    )
    
    # Detailed description of the community
    description = models.TextField(
        help_text="Detailed description of what this community is about"
    )
    
    # Flag to indicate if this is a parent (top-level) community
    is_parent = models.BooleanField(
        default=True, 
        help_text="Is this a parent community? (False for subcommunities)"
    )
    
    # Self-referential foreign key for hierarchical structure
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcommunities',
        help_text="Parent community (leave blank for top-level communities)"
    )

    # Timestamp fields for tracking creation and updates
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this community was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this community was last updated"
    )

    def save(self, *args, **kwargs):
        """
        Custom save method to auto-generate slug and color
        
        This method is called every time a Community instance is saved.
        It automatically generates a URL-friendly slug from the title
        and assigns a random color if one isn't already set.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Process:
            1. Generate slug from title if not already set
            2. Generate random color if not already set  
            3. Call parent save method to actually save to database
        """
        if not self.slug:
            # Generate URL-friendly slug from title
            # e.g., "Computer Science" becomes "computer-science"
            self.slug = slugify(self.title)
            
        if not self.color:
            # Assign random color for space visualization
            self.color = generate_random_color()
            
        # Call the parent save method to actually save to database
        super().save(*args, **kwargs)

    def memeber_count(self):
        """
        Get the number of members in this community
        
        Returns:
            int: Number of users who are members of this community
            
        Note: There's a typo in the method name - should be "member_count"
        """
        return self.members.count()
    
    def __str__(self):
        """
        String representation of the Community model
        
        Returns:
            str: The community title
            
        This is used in Django admin and when converting Community
        instances to strings for display purposes.
        """
        return self.title
    

class Membership(models.Model):
    """
    Membership Model for User-Community Relationships
    
    This model represents the many-to-many relationship between Users
    and Communities. It tracks which users are members of which communities
    and when they joined.
    
    This is implemented as a separate model (rather than Django's built-in
    ManyToManyField) to allow for additional fields like join timestamp
    and potential future fields like membership role, permissions, etc.
    
    Fields:
        user: Foreign key to the User who is a member
        community: Foreign key to the Community they joined
        joined_at: Timestamp of when they joined the community
    
    Constraints:
        - A user can only be a member of a community once (unique_together)
        - If user or community is deleted, the membership is also deleted (CASCADE)
    """
    
    # User who is a member of the community
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="The user who is a member of this community"
    )
    
    # Community that the user is a member of
    community = models.ForeignKey(
        Community, 
        on_delete=models.CASCADE, 
        related_name='members',
        help_text="The community this user is a member of"
    )
    
    # Timestamp of when the user joined the community
    joined_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this user joined the community"
    )

    class Meta:
        """
        Meta configuration for Membership model
        
        Defines database constraints and behavior for the model.
        """
        # Ensure a user can only be a member of a community once
        unique_together = ('user', 'community')
        
        # Optional: Add verbose names for Django admin
        verbose_name = "Community Membership"
        verbose_name_plural = "Community Memberships"

    def __str__(self):
        """
        String representation of the Membership model
        
        Returns:
            str: Description of the membership relationship
        """
        return f"{self.user.username} is a member of {self.community.title}"


class Post(models.Model):
    """
    Post Model for Community Content
    
    This model represents content posted by users within communities.
    Posts are the primary way users share information, ask questions,
    start discussions, and collaborate within their academic communities.
    
    Fields:
        community: The community where this post was made
        author: The user who created this post
        content: The actual text content of the post
        created_at: When the post was created
    
    Future enhancements could include:
        - Post titles for longer content
        - File attachments (images, documents)
        - Post categories or tags
        - Like/upvote system
        - Comment threading
        - Post editing timestamps
    """
    
    # Community where this post was made
    community = models.ForeignKey(
        Community, 
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The community where this post was made"
    )
    
    # User who created this post
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The user who created this post"
    )
    
    # Content of the post
    content = models.TextField(
        help_text="The text content of the post"
    )
    
    # When the post was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this post was created"
    )

    class Meta:
        """
        Meta configuration for Post model
        """
        # Order posts by newest first
        ordering = ['-created_at']
        
        # Verbose names for Django admin
        verbose_name = "Community Post"
        verbose_name_plural = "Community Posts"

    def __str__(self):
        """
        String representation of the Post model
        
        Returns:
            str: Description of the post with truncated content
        """
        # Truncate content to first 50 characters for display
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Post by {self.author.username} in {self.community.title}: {content_preview}"


