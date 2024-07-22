from rest_framework import serializers
from .models import Character, Diary


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "name", "character_type", "user"]


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = [
            "id",
            "user",
            "content",
            "entry_time",
            "date",
            "weather",
            "wake_up_time",
            "sleep_time",
        ]


class ActionSerializer(serializers.Serializer):
    ACTION_CHOICES = [
        ("eating", "밥 먹기"),
        ("cleaning", "청소하기"),
        ("walking", "산책하기"),
        ("washing", "씻기"),
    ]

    action_type = serializers.ChoiceField(choices=ACTION_CHOICES)
    detail = serializers.CharField(max_length=200)

    def validate(self, data):
        if data["action_type"] == "washing" and data["detail"] not in ["yes", "no"]:
            raise serializers.ValidationError("Invalid detail for washing action")
        return data
