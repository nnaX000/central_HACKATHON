from django.contrib import admin
from .models import Post, UserProfile
from main.models import Notification


admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(UserProfile)
