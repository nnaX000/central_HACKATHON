from rest_framework import serializers
from main.models import Notification  
from post.models import Post  

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'date_posted', 'author', 'total_likes'] 

class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    sender = serializers.StringRelatedField()  
    recipient = serializers.StringRelatedField() 

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'post', 'message', 'created_at', 'read']
