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
    CharacterListCreateView,
    CharacterDetailView,
    CharacterGaugeView,
    JournalEntryListCreateView,
    JournalEntryDetailView,
    EndingListCreateView,
    EndingDetailView,
    DiaryEntryListCreateView,
    DiaryEntryDetailView,
    CharacterEndingView,
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
    path(
        "characters/", CharacterListCreateView.as_view(), name="character-list-create"
    ),
    path(
        "characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"
    ),
    path("characters/gauge/", CharacterGaugeView.as_view(), name="character-gauge"),
    path(
        "journal_entries/",
        JournalEntryListCreateView.as_view(),
        name="journal-entry-list-create",
    ),
    path(
        "journal_entries/<int:pk>/",
        JournalEntryDetailView.as_view(),
        name="journal-entry-detail",
    ),
    path("endings/", EndingListCreateView.as_view(), name="ending-list-create"),
    path("endings/<int:pk>/", EndingDetailView.as_view(), name="ending-detail"),
    path(
        "diary_entries/",
        DiaryEntryListCreateView.as_view(),
        name="diary-entry-list-create",
    ),
    path(
        "diary_entries/<int:pk>/",
        DiaryEntryDetailView.as_view(),
        name="diary-entry-detail",
    ),
    path("character/ending/", CharacterEndingView.as_view(), name="character-ending"),
    # ---------------------------------------------------------------------------------
    # post
    path("post/", include("post.urls")),
    # ----------------------------------------
    # board
    path("board/", include("board.urls")),
    # ----------------------------------------
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
