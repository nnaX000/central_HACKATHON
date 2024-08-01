from rest_framework import serializers
from character.models import JournalEntry, Character
from .models import EveryList, LifeList

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'character', 'date', 'action_type', 'meal_time', 'action_detail', 'completed']

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'type', 'gauge', 'active']

class EveryListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EveryList
        fields = ['id', 'user', 'task', 'due_date', 'due_time', 'completed', 'created_at', 'updated_at']

class LifeListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LifeList
        fields = '__all__'
        read_only_fields = ['user']