from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('posthome/', views.posthome, name='posthome'),
    path('create/', views.post_create, name='post_create'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('user/posts/', views.user_posts, name='user_posts'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('notifications/', views.notifications, name='notifications'),
     path('notifications/read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
