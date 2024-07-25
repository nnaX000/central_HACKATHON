from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Post, Notification, UserProfile
from .serializers import PostSerializer, NotificationSerializer
from django.core.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if not user_profile.can_post:
            raise PermissionDenied(f'You are banned from posting until {user_profile.ban_until}')
        serializer.save(author=self.request.user)

@api_view(['GET'])
def posthome(request):
    sort_by = request.GET.get('sort', 'date')
    category = request.GET.get('category', 'latest')
    
    if category == 'my_posts':
        posts = Post.objects.filter(author=request.user)
    elif category == 'liked_posts':
        posts = Post.objects.filter(likes=request.user)
    else:
        posts = Post.objects.all()
    
    if sort_by == 'likes':
        posts = sorted(posts, key=lambda post: post.total_likes, reverse=True)
    else:
        posts = posts.order_by('-date_posted')
    
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
    return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

        # 좋아요 알림 생성
        if user != post.author:
            try:
                notification = Notification.objects.create(
                    user=post.author,
                    post=post,
                    message=f"{user.username}님이 '{post.title}' 글을 좋아합니다."
                )
                logger.info(f"알림 생성: {notification.message} (ID: {notification.id})")
            except Exception as e:
                logger.error(f"알림 생성 오류: {e}")
                return Response({'error': f"알림 생성 오류: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'liked': liked,
        'total_likes': post.likes.count(),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.read = True
    notification.save()
    return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.reports.filter(id=user.id).exists():
        return Response({'message': 'You have already reported this post.'}, status=status.HTTP_400_BAD_REQUEST)

    post.reports.add(user)
    post.total_reports += 1
    post.save()

    if post.total_reports >= 10:
        post.delete()
        user_profile, created = UserProfile.objects.get_or_create(user=post.author)
        user_profile.ban_user_for_one_week()

    return Response({'message': 'Post reported successfully'}, status=status.HTTP_200_OK)
