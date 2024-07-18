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
from django.contrib.auth import update_session_auth_hash

logger = logging.getLogger(__name__)


# 회원가입
@csrf_exempt
def signup(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
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


# 아이디 중복 검사
@require_http_methods(["POST"])
def check_user_id(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")
    if CustomUser.objects.filter(user_id=user_id).exists():
        return JsonResponse({"user_id_exists": True})
    else:
        return JsonResponse({"user_id_exists": False})


# 로그인
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


# 비밀번호를 바꾸기 위한 이메일 주소 확인
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST["email"]
        associated_user = CustomUser.objects.filter(email=email).first()
        if associated_user:
            return render(request, "password_reset_form.html", {"email": email})
        else:
            return render(
                request,
                "password_reset_request.html",
                {"error": "해당 이메일 주소가 없습니다."},
            )
    return render(request, "password_reset_request.html")


# 비밀번호 바꾸기
def password_reset_confirm(request):
    if request.method == "POST":
        email = request.POST["email"]
        new_password1 = request.POST["new_password1"]
        new_password2 = request.POST["new_password2"]
        if new_password1 == new_password2:
            associated_user = CustomUser.objects.filter(email=email).first()
            if associated_user:
                associated_user.set_password(new_password1)
                associated_user.save()
                return redirect("login")
            else:
                return render(
                    request,
                    "password_reset_form.html",
                    {"error": "해당 이메일 주소가 없습니다.", "email": email},
                )
        else:
            return render(
                request,
                "password_reset_form.html",
                {"error": "비밀번호가 일치하지 않습니다.", "email": email},
            )
    return render(request, "password_reset_form.html")
    if request.method == "POST":
        email = request.POST["email"]
        new_password1 = request.POST["new_password1"]
        new_password2 = request.POST["new_password2"]
        if new_password1 == new_password2:
            associated_user = CustomUser.objects.filter(email=email).first()
            if associated_user:
                associated_user.set_password(new_password1)
                associated_user.save()
                return redirect("login")
            else:
                return render(
                    request,
                    "password_reset_form.html",
                    {"error": "해당 이메일 주소가 없습니다.", "email": email},
                )
        else:
            return render(
                request,
                "password_reset_form.html",
                {"error": "비밀번호가 일치하지 않습니다.", "email": email},
            )
    return render(request, "password_reset_form.html")


@login_required
def profile_view(request):
    return render(request, "mypage.html")


# 프로필 사진 수정
@login_required
def profile_edit(request):
    if request.method == "POST":
        photo = request.FILES.get("photo")
        if photo:
            request.user.photo = photo
            request.user.save()
            messages.success(request, "프로필 사진이 수정되었습니다.")
        return redirect("mypage")
    return render(request, "profile_edit.html")


# 개인 정보 수정
@login_required
def personal_info_edit(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password and password != password2:
            return render(
                request,
                "personal_info_edit.html",
                {"error": "비밀번호가 일치하지 않습니다."},
            )

        # ID 중복 검사
        if (
            CustomUser.objects.filter(user_id=user_id)
            .exclude(pk=request.user.pk)
            .exists()
        ):
            return render(
                request, "personal_info_edit.html", {"error": "이미 존재하는 ID입니다."}
            )

        request.user.user_id = user_id
        request.user.username = username
        request.user.email = email

        if password:
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(
                request, request.user
            )  # 비밀번호 변경 후에도 세션 유지
            messages.success(
                request, "비밀번호가 변경되었습니다. 다시 로그인 해주세요."
            )
            return redirect("login")

        request.user.save()
        messages.success(request, "프로필이 성공적으로 수정되었습니다.")
        return redirect("mypage")

    return render(request, "personal_info_edit.html")
