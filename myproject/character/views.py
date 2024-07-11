from django.shortcuts import render, redirect, HttpResponse
from .models import Character
from .forms import CharacterForm, ActionForm
from django.contrib import messages


# 게임홈화면
def game(request, id=None):
    if id:
        characters = [Character.objects.get(id=id)]
    else:
        characters = Character.objects.all()

    return render(request, "game.html", {"characters": characters})


# 캐릭터 생성
def create_character(request):
    existing_character = Character.objects.filter(gauge__lt=100).first()
    if existing_character:
        return HttpResponse("이미 활동 중인 캐릭터가 있습니다. 게이지를 완료하세요.")

    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("game")
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


# update_action페이지 안에서 행동 페이지로 가는 함수
def handle_action(request, id, action, action_name):
    character = Character.objects.get(id=id)
    if request.method == "POST":
        detail = request.POST.get("detail")
        character.current_action = f"{action_name}: {detail}"
        character.gauge += 100
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


# 캐릭터 행동하기
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
