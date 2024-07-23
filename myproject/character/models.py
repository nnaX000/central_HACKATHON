from django.db import models
from django import forms
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Character(models.Model):
    CHARACTER_TYPES = [
        ("parrot", "앵무새"),
        ("dolphin", "돌고래"),
        ("squirrel", "다람쥐"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CHARACTER_TYPES, default="parrot")
    gauge = models.PositiveIntegerField(default=0)  # 캐릭터 게이지
    active = models.BooleanField(default=True)  # 활성화 여부

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class JournalEntry(models.Model):
    ACTION_TYPES = [
        ("eat", "먹기"),
        ("wash", "씻기"),
        ("walk", "산책하기"),
        ("shower", "샤워하기"),
    ]

    MEAL_TIMES = [
        ("breakfast", "아침"),
        ("lunch", "점심"),
        ("dinner", "저녁"),
        ("snack", "간식"),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now().date)  # 날짜 필드를 기본값으로 설정
    action_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    meal_time = models.CharField(
        max_length=10, choices=MEAL_TIMES, null=True, blank=True
    )
    action_detail = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.get_action_type_display()}"


class Ending(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    journal_entries = models.TextField()  # JSON 또는 텍스트 형태로 모든 기록을 저장

    def __str__(self):
        return f"Ending for {self.character.name} on {self.date}"


class DiaryEntry(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now().date)  # 날짜 필드를 기본값으로 설정
    weather = models.CharField(max_length=100, null=True, blank=True)  # 날씨 필드 추가
    diary_text = models.TextField()  # 일기 필드 추가

    def __str__(self):
        return f"{self.date} - {self.character.name}"
