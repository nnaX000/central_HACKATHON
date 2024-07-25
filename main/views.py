from django.shortcuts import render


# 홈화면으로
def home(request):
    return render(request, "home.html")

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from board.models import EveryList, LifeList
from board.serializers import EveryListSerializer, LifeListSerializer
from main.models import Notification 
from post.models import Post
from .serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def combined_list_view(request):
    user = request.user
    everylist_items = EveryList.objects.filter(user=user)
    lifelist_items = LifeList.objects.filter(user=user)

    everylist_serializer = EveryListSerializer(everylist_items, many=True)
    lifelist_serializer = LifeListSerializer(lifelist_items, many=True)

    return Response({
        'everylist': everylist_serializer.data,
        'lifelist': lifelist_serializer.data
    })

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