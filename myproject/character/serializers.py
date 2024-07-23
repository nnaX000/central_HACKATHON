from rest_framework import serializers
from .models import Character, JournalEntry, Ending, DiaryEntry


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "user", "name", "type", "gauge", "active"]


class JournalEntrySerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        format="%Y-%m-%d", read_only=True
    )  # 날짜 필드 형식 지정

    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "character",
            "date",
            "action_type",
            "meal_time",
            "action_detail",
            "completed",
        ]


class EndingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ending
        fields = ["id", "character", "date", "journal_entries"]


class DiaryEntrySerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        format="%Y-%m-%d", read_only=True
    )  # 날짜 필드 형식 지정

    class Meta:
        model = DiaryEntry
        fields = ["id", "character", "date", "weather", "diary_text"]
