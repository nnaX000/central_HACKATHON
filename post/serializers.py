from rest_framework import serializers
from .models import Post, Notification

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'date_posted', 'author']
        read_only_fields = ['author', 'date_posted']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'post', 'message', 'created_at', 'read']
