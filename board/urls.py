from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EveryListView, EveryListDetailView, LifeListView, LifeListDetailView, RecommendView, recommend_page, AddRecommendationToListView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

urlpatterns = [
    path('recommend/', RecommendView.as_view(), name='recommend'),
    path('recommend_page/', recommend_page, name='recommend_page'),
    path('add_recommendations/', AddRecommendationToListView.as_view(), name='add-recommendations'),
    path('everylist/', EveryListView.as_view(), name='everylist-list-create'),
    path('everylist/<int:pk>/', EveryListDetailView.as_view(), name='everylist-detail'),
    path('lifelist/', LifeListView.as_view(), name='lifelist-list-create'),
    path('lifelist/<int:pk>/', LifeListDetailView.as_view(), name='lifelist-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
