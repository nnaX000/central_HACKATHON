from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        photo = request.FILES.get("photo", None)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "Username already exists"}, status=400
            )

        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
        if photo:
            user.photo = photo
            user.save()

        return JsonResponse({"success": "User registered successfully"})

    return render(request, "signup.html")
