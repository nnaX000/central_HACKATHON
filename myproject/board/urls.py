from django.urls import path
from  . import views

urlpatterns = [
    path('recommend/', views.RecommendView.as_view(), name='recommend'),
    path('recommend_page/', views.recommend_page, name='recommend_page'),

]
