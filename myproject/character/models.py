from django.db import models
from django import forms
from django.conf import settings


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

    YES_NO_CHOICES = [
        ("yes", "예"),
        ("no", "아니오"),
    ]

    action_type = forms.ChoiceField(choices=ACTION_CHOICES, label="행동 선택")
    detail = forms.CharField(
        max_length=200,
        label="상세 내용",
        widget=forms.TextInput(attrs={"placeholder": "여기에 입력"}),
    )

    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        if self.data.get("action_type") == "washing":
            self.fields["detail"] = forms.ChoiceField(
                choices=self.YES_NO_CHOICES, label="상세 내용", widget=forms.RadioSelect
            )


class Diary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 변경된 부분
    content = models.TextField()
    entry_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    weather = models.CharField(
        max_length=20,
        choices=[
            ("sunny", "맑음"),
            ("partly_cloudy", "약간 흐림"),
            ("cloudy", "흐림"),
            ("rain", "비"),
            ("snow", "눈"),
        ],
    )
    wake_up_time = models.TimeField()
    sleep_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"
