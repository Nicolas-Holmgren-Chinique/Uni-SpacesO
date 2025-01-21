from django.db import models

class HomeContent(models.Model):
    TITLE_CHOICE = [
        ('home', 'Home'),
        ('base', 'Base'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TITLE_CHOICE)

    def __str__(self):
        return self.title
