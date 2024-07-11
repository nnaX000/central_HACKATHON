from django.db import models
from django import forms


class Character(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    current_action = models.CharField(max_length=200, blank=True)
    gauge = models.IntegerField(default=0)
    final_action = models.TextField(blank=True)  # 추가

    def __str__(self):
        return self.name


class ActionForm(forms.Form):
    ACTION_CHOICES = [
        ("eating", "밥 먹기"),
        ("cleaning", "청소하기"),
        ("walking", "산책하기"),
        ("washing", "씻기"),
    ]

    action_type = forms.ChoiceField(choices=ACTION_CHOICES, label="행동 선택")
    detail = forms.CharField(
        max_length=200,
        label="상세 내용",
        widget=forms.TextInput(attrs={"placeholder": "여기에 입력"}),
    )
