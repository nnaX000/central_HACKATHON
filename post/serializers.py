from rest_framework import serializers
from .models import Post
from main.models import Notification 
from user.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='profile_image.url', read_only=True)  # Assuming 'profile_image' is the field name for profile images in UserProfile model.

    class Meta:
        model = CustomUser
        fields = ['profile_image']

class PostSerializer(serializers.ModelSerializer):
    author_profile = UserProfileSerializer(source='author.userprofile', read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'date_posted', 'author_username',  'author_profile', 'likes', 'total_likes']
        read_only_fields = ['author', 'date_posted']

    def get_author_username(self, obj):
        return obj.author.username 
    
    def get_total_likes(self, obj):
        return obj.likes.count()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'post', 'message', 'created_at', 'read']


