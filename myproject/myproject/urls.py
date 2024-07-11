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
from character.views import (
    game,
    create_character,
    action_eating,
    action_cleaning,
    action_walking,
    action_washing,
    update_action,
    finalize_action,
)


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("home/", home, name="home"),
    path("logout/", logout_view, name="logout"),
    path("delete_account/", delete_account_view, name="delete_account"),
    path("mypage/", mypage, name="mypage"),
    path("check_user_id/", check_user_id, name="check_user_id"),
    # character
    path("game/<int:id>/", game, name="game"),
    path("game/", game, name="game"),
    path("create/", create_character, name="create_character"),
    path("character/<int:id>/eating/", action_eating, name="action_eating"),
    path("character/<int:id>/cleaning/", action_cleaning, name="action_cleaning"),
    path("character/<int:id>/walking/", action_walking, name="action_walking"),
    path("character/<int:id>/washing/", action_washing, name="action_washing"),
    path("update_action/<int:id>/", update_action, name="update_action"),
    path("character/<int:id>/finalize/", finalize_action, name="finalize_action"),
    # ---------------------------------------------------------------------------------
]
