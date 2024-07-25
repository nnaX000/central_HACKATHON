from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="post_images/")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_likes", blank=True
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_bookmarks", blank=True
    )
    reports = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_reports", blank=True
    )
    total_reports = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_notifications', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username} on {self.post.title}"
    

    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    can_post = models.BooleanField(default=True)
    ban_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def ban_user_for_one_week(self):
        self.can_post = False
        self.ban_until = datetime.now() + timedelta(days=7)
        self.save()

    def unban_user(self):
        if self.ban_until and datetime.now() > self.ban_until:
            self.can_post = True
            self.ban_until = None
            self.save()
