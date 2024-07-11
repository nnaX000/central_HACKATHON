from django.shortcuts import render, redirect, HttpResponse
from .models import Character
from .forms import CharacterForm, ActionForm
from django.contrib import messages


def game(request, id=None):
    if id:
        characters = [Character.objects.get(id=id)]
    else:
        characters = Character.objects.all()

    return render(request, "game.html", {"characters": characters})


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


def get_action_label(action):
    return {
        "eating": "밥 먹기",
        "cleaning": "청소하기",
        "walking": "산책하기",
        "washing": "씻기",
    }[action]


def complete_action(request, id):
    character = Character.objects.get(id=id)
    character.gauge = 0  # Reset gauge
    character.save()
    return render(request, "complete_action.html", {"character": character})


def action_eating(request, id):
    return handle_action(request, id, "eating", "밥 먹기")


def action_cleaning(request, id):
    return handle_action(request, id, "cleaning", "청소하기")


def action_walking(request, id):
    return handle_action(request, id, "walking", "산책하기")


def action_washing(request, id):
    return handle_action(request, id, "washing", "씻기")


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


def update_action(request, id):
    character = Character.objects.get(id=id)
    if request.method == "POST":
        action = request.POST.get("action")
        detail = request.POST.get("detail")
        action_label = get_action_label(action)
        character.current_action = f"{action_label}: {detail}"
        character.gauge += 100
        character.save()
        if character.gauge >= 100:
            return redirect("complete_action", id=character.id)
        return redirect("game")
    return render(request, "update_action.html", {"character": character})


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
