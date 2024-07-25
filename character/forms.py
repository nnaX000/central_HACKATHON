from django import forms
from .models import Character


class CharacterForm(forms.ModelForm):
    CHARACTER_CHOICES = [
        ("dol", "돌고래"),
        ("ang", "앵무새"),
        ("da", "다람쥐"),
    ]
    character_type = forms.ChoiceField(
        choices=CHARACTER_CHOICES, widget=forms.RadioSelect
    )
    name = forms.CharField(max_length=100)

    class Meta:
        model = Character
        fields = ["name", "character_type"]


class ActionForm(forms.Form):
    action = forms.CharField(max_length=200, required=True)
