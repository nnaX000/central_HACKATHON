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

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from user.views import user_views
from user.views import (
    SignupView,
    LoginView,
    MyPageView,
    CheckUserIDView,
    LogoutView,
    BookmarksView,
    DeleteAccountView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfileEditView,
    PersonalInfoEditView,
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
    diary_entry,
    view_diaries,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # account
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("check_user_id/", CheckUserIDView.as_view(), name="check_user_id"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("bookmarks/", BookmarksView.as_view(), name="bookmarks"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete_account"),
    path(
        "password-reset-request/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("profile-edit/", ProfileEditView.as_view(), name="profile_edit"),
    path(
        "personal-info-edit/", PersonalInfoEditView.as_view(), name="personal_info_edit"
    ),
    # ---------------------------------------------------------------------------------
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
    path("diary/entry/", diary_entry, name="diary_entry"),
    path("diary/view/", view_diaries, name="view_diaries"),
    # ---------------------------------------------------------------------------------
    # post
    path("post/", include("post.urls")),
    # ----------------------------------------
    # board
    path("board/", include("board.urls")),
    # ----------------------------------------
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
