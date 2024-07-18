from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.posthome, name='posthome'),
    path('create/', views.post_create, name='post_create'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    # path('bookmark/<int:pk>/', views.bookmark_post, name='bookmark_post'),
    # path('bookmarked/', views.bookmarked_posts, name='bookmarked_posts'),
    path('my_posts/', views.user_posts, name='user_posts'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)