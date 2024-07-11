from django import forms
from .models import Character


class CharacterForm(forms.ModelForm):
    GENDER_CHOICES = [
        ("male", "남자"),
        ("female", "여자"),
        ("unspecified", "선택 안함"),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Character
        fields = ["name", "age", "gender", "current_action"]


class ActionForm(forms.Form):
    action = forms.CharField(max_length=200, required=True)
