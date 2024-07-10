"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

# from user.views import user_views
from user.views import (
    signup,
    user_login,
    logout_view,
    delete_account_view,
    mypage,
    check_user_id,
)
from main.views import home


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("home/", home, name="home"),
    path("logout/", logout_view, name="logout"),
    path("delete_account/", delete_account_view, name="delete_account"),
    path("mypage/", mypage, name="mypage"),
    path("check_user_id/", check_user_id, name="check_user_id"),
]
