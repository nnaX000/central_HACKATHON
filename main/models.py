# main/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from post.models import Post

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='main_notifications', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='main_notifications', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username} on {self.post.title if self.post else 'No Post'}"
