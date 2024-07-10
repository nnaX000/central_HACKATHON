from django.shortcuts import render


# 홈화면으로
def home(request):
    return render(request, "home.html")
