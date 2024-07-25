from django.contrib import admin
from .models import Post, Notification, UserProfile

admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(UserProfile)
