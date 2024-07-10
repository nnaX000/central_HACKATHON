from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        photo = request.FILES.get("photo", None)

        if CustomUser.objects.filter(user_id=user_id).exists():
            return JsonResponse(
                {"user_id_error": "이미 존재하는 ID입니다."}, status=400
            )

        user = CustomUser.objects.create_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            photo=photo,
        )

        return JsonResponse({"message": "환영합니다!"})  # 성공 메시지 전송

    return render(request, "signup.html")


@require_http_methods(["POST"])
def check_user_id(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")
    if CustomUser.objects.filter(user_id=user_id).exists():
        return JsonResponse({"user_id_exists": True})
    else:
        return JsonResponse({"user_id_exists": False})


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(user_id=user_id)
            if user.check_password(password):
                login(request, user, backend="user.authentication.UserIDAuthBackend")
                return redirect("home")
            else:
                return render(
                    request, "login.html", {"error": "잘못된 비밀번호입니다."}
                )
        except CustomUser.DoesNotExist:
            return render(
                request, "login.html", {"error": "존재하지 않는 사용자 ID입니다."}
            )

    return render(request, "login.html", {"error": ""})


# 로그아웃
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")  # 로그아웃 후 리디렉션 될 페이지


# 계정탈퇴
@login_required
def delete_account_view(request):
    # 사용자 요청에 따라 계정 삭제
    user = request.user
    user.delete()

    # 사용자 로그아웃
    logout(request)

    # 사용자에게 알림 메시지 전달
    messages.success(request, "계정이 성공적으로 삭제되었습니다.")

    # 로그인 페이지로 리디렉션
    return redirect("login")


# 북마크한 글 볼 수 있게
@login_required
def bookmarks_view(request):
    # 북마크한 글을 불러오는 로직 구현
    return render(request, "bookmarks.html", {})


# 마이페이지로
def mypage(request):
    # 북마크한 글을 불러오는 로직 구현
    return render(request, "mypage.html")
