from rest_framework import serializers
from main.models import Notification  
from post.models import Post  
from user.models import CustomUser


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'date_posted', 'author', 'total_likes']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'photo']

class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    sender = UserSerializer(read_only=True) 
    recipient = serializers.StringRelatedField() 

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'post', 'message', 'created_at', 'read']