from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth import authenticate, login


@csrf_exempt
def signup(request):
    if request.method == "POST":
        user_id = request.POST["id"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        photo = request.FILES.get("photo", None)

        if CustomUser.objects.filter(user_id=user_id).exists():
            return JsonResponse({"username_error": "UserID already exists"}, status=400)

        user = CustomUser.objects.create(
            user_id=user_id,
            username=username,
            email=email,
            password=make_password(password),
        )
        if photo:
            user.photo = photo
            user.save()

        return redirect("login")

    return render(request, "signup.html")


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        password = request.POST["password"]

        # authenticate 함수에 user_id를 전달
        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # 로그인 성공 시 홈 페이지로 리다이렉트
        else:
            return render(
                request,
                "login.html",
                {"error": "잘못된 사용자 ID 또는 비밀번호입니다."},
            )

    return render(request, "login.html")
