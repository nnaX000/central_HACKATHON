from django.shortcuts import render, redirect, HttpResponse
from .models import Character, Diary
from .forms import CharacterForm, ActionForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime


# 게임홈화면
def game(request, id=None):
    if id:
        characters = [Character.objects.get(id=id)]
    else:
        characters = Character.objects.all()

    return render(request, "game.html", {"characters": characters})


# 캐릭터 생성/form data
@csrf_exempt
def create_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            print("Saving character: ", instance.__dict__)
            instance.save()
            return redirect("game")
        else:
            print("Form errors: ", form.errors)
    else:
        form = CharacterForm()
    return render(request, "create_character.html", {"form": form})


# 액션 리스트
def get_action_label(action):
    return {
        "eating": "밥 먹기",
        "cleaning": "청소하기",
        "walking": "산책하기",
        "washing": "씻기",
    }[action]


# update_action페이지까지 가는 함수
def update_action(request, id):
    character = Character.objects.get(id=id)
    return render(request, "update_action.html", {"character": character})


# update_action페이지 안에서 행동 페이지로 가는 함수/form data
def handle_action(request, id, action, action_name):
    character = Character.objects.get(id=id)
    if request.method == "POST":
        detail = request.POST.get("detail")
        character.current_action = f"{action_name}: {detail}"
        character.gauge += 5
        character.save()
        if character.gauge >= 100:
            return redirect("game", id=character.id)
        return redirect("game")
    return render(
        request,
        "action_detail.html",
        {"character": character, "action_name": action_name},
    )


# 먹기
def action_eating(request, id):
    return handle_action(request, id, "eating", "밥 먹기")


# 청소하기
def action_cleaning(request, id):
    return handle_action(request, id, "cleaning", "청소하기")


# 걷기
def action_walking(request, id):
    return handle_action(request, id, "walking", "산책하기")


# 씻기
def action_washing(request, id):
    return handle_action(request, id, "washing", "씻기")


# 캐릭터 행동하기/form data
def finalize_action(request, id):
    character = Character.objects.get(id=id)
    if request.method == "POST":
        final_action = request.POST.get("final_action")
        character.final_action = final_action
        character.save()
        character.delete()  # 캐릭터 삭제
        messages.success(
            request, "활기찬 캐릭터가 완성되었네요! 새로운 캐릭터로 활동해볼까요?"
        )
        return redirect("game")
    else:
        return render(request, "finalize_action.html", {"character": character})


# 일기 등록
def diary_entry(request):
    if request.method == "POST":
        try:
            diary = Diary(
                user=request.user,
                content=request.POST.get("content"),
                date=datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date(),
                weather=request.POST.get("weather"),
                wake_up_time=datetime.strptime(
                    request.POST.get("wake_up_time"), "%H:%M"
                ).time(),
                sleep_time=datetime.strptime(
                    request.POST.get("sleep_time"), "%H:%M"
                ).time(),
            )
            diary.save()
            return redirect("view_diaries")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return render(request, "diary_entry.html")


# 일기 보기
@login_required
def view_diaries(request):
    diaries = Diary.objects.filter(user=request.user)
    return render(request, "view_diary.html", {"diaries": diaries})
