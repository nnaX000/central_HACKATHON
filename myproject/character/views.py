# views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Character, JournalEntry, Ending, DiaryEntry
from .serializers import (
    CharacterSerializer,
    JournalEntrySerializer,
    EndingSerializer,
    DiaryEntrySerializer,
)


class CharacterListCreateView(generics.ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)


class CharacterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)


class CharacterGaugeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        character = get_object_or_404(Character, user=request.user, active=True)
        return Response({"gauge": character.gauge}, status=status.HTTP_200_OK)


class JournalEntryListCreateView(generics.ListCreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        character = get_object_or_404(Character, id=self.request.data.get("character"))
        if character.user == self.request.user:
            serializer.save(character=character, date=timezone.now().date())
            character.gauge += 5
            character.save()
        else:
            raise PermissionDenied(
                "You do not have permission to add entries for this character."
            )

    def get_queryset(self):
        return JournalEntry.objects.filter(character__user=self.request.user)


class JournalEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(character__user=self.request.user)


class EndingListCreateView(generics.ListCreateAPIView):
    queryset = Ending.objects.all()
    serializer_class = EndingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        character = get_object_or_404(Character, id=self.request.data.get("character"))
        if character.user == self.request.user:
            journal_entries = JournalEntry.objects.filter(character=character).order_by(
                "date"
            )
            diary_entries = DiaryEntry.objects.filter(character=character).order_by(
                "date"
            )
            serializer.save(
                character=character,
                journal_entries=journal_entries,
                diary_entries=diary_entries,
            )
        else:
            raise PermissionDenied(
                "You do not have permission to create an ending for this character."
            )

    def get_queryset(self):
        return Ending.objects.filter(character__user=self.request.user)


class EndingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ending.objects.all()
    serializer_class = EndingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ending.objects.filter(character__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        journal_entries = JournalEntry.objects.filter(
            character=instance.character
        ).order_by("date")
        journal_data = JournalEntrySerializer(journal_entries, many=True).data
        diary_entries = DiaryEntry.objects.filter(
            character=instance.character
        ).order_by("date")
        diary_data = DiaryEntrySerializer(diary_entries, many=True).data
        data = serializer.data
        data["journal_entries"] = journal_data
        data["diary_entries"] = diary_data
        return Response(data)


class DiaryEntryListCreateView(generics.ListCreateAPIView):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        character = get_object_or_404(Character, id=self.request.data.get("character"))
        if character.user == self.request.user:
            serializer.save(character=character, date=timezone.now().date())
        else:
            raise PermissionDenied(
                "You do not have permission to add entries for this character."
            )

    def get_queryset(self):
        return DiaryEntry.objects.filter(character__user=self.request.user)


class DiaryEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiaryEntry.objects.filter(character__user=self.request.user)


class CharacterEndingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        character = get_object_or_404(Character, user=request.user, active=True)
        journal_entries = JournalEntry.objects.filter(character=character).order_by(
            "date"
        )
        diary_entries = DiaryEntry.objects.filter(character=character).order_by("date")

        data = []
        for date in sorted(
            set(entry.date for entry in journal_entries)
            | set(entry.date for entry in diary_entries)
        ):
            day_data = {
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "weather": "맑음",  # 날씨는 사용자가 입력하도록 설계해야 함
                "meals": {"breakfast": "", "lunch": "", "dinner": "", "snack": ""},
                "records": {"cleaning": "", "exercise": "", "shower": ""},
                "diary": "",
            }

            for entry in journal_entries.filter(date=date):
                if entry.action_type == "eat":
                    if entry.meal_time:
                        day_data["meals"][entry.meal_time] = entry.action_detail
                elif entry.action_type == "wash":
                    day_data["records"]["cleaning"] = entry.action_detail
                elif entry.action_type == "walk":
                    day_data["records"]["exercise"] = entry.action_detail
                elif entry.action_type == "shower":
                    day_data["records"]["shower"] = entry.action_detail

            for diary in diary_entries.filter(date=date):
                day_data["diary"] = diary.diary_text

            data.append(day_data)

        return Response(data)
