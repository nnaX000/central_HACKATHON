from rest_framework import serializers
from .models import Post, Notification

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'date_posted', 'author', 'likes', 'total_likes']
        read_only_fields = ['author', 'date_posted']

    def get_total_likes(self, obj):
        return obj.likes.count()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'post', 'message', 'created_at', 'read']


