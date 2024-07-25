from rest_framework import serializers
from .models import Notification
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title'] 


class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True) 
    class Meta:
        model = Notification
        fields = '__all__'


        