from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StudyRoom(models.Model):
    name = models.CharField(max_length=100, default="Study Room")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class RoomParticipant(models.Model):
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"

class RoomMessage(models.Model):
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class StudyBlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_blocks')
    title = models.CharField(max_length=200)
    day_index = models.IntegerField(null=True, blank=True) # 0=Monday, 6=Sunday (For recurring)
    date = models.DateField(null=True, blank=True) # For specific dates
    start_date = models.DateField(null=True, blank=True) # Range start for recurring
    end_date = models.DateField(null=True, blank=True) # Range end for recurring
    start_hour = models.FloatField() # 0-23.5
    duration = models.FloatField() # hours
    block_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('ai', 'AI')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
