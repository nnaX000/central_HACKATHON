# views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from urllib.parse import unquote
from .models import (
    Character,
    JournalEntry,
    Ending,
    DiaryEntry,
    Food,
    CleaningSpot,
    WalkingPlace,
)
from .serializers import (
    CharacterSerializer,
    JournalEntrySerializer,
    EndingSerializer,
    DiaryEntrySerializer,
)
from rest_framework.exceptions import ValidationError
import random


class CharacterListCreateView(generics.ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 현재 활성화된 캐릭터가 있는지 확인
        if Character.objects.filter(
            user=self.request.user, active=True, ended=False
        ).exists():
            raise ValidationError("활성화된 캐릭터가 이미 있습니다.")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user, ended=False)


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
        action_type = self.request.data.get("action_type")
        action_detail = self.request.data.get("action_detail")
        action_completed = self.request.data.get("completed")

        if character.user == self.request.user:
            serializer.save(
                character=character,
                date=timezone.now().date(),
                completed=action_completed,
            )
            character.gauge += 5
            character.save()

            # 행동 기록에 새로운 항목을 추가
            if (
                action_type == "eat"
                and not Food.objects.filter(name=action_detail).exists()
            ):
                if action_detail:
                    Food.objects.create(name=action_detail)
                else:
                    print("Food action_detail is empty or invalid")

            elif (
                action_type == "cleaning"
                and not CleaningSpot.objects.filter(name=action_detail).exists()
            ):
                if action_detail:
                    CleaningSpot.objects.create(name=action_detail)
                else:
                    print("CleaningSpot action_detail is empty or invalid")

            elif (
                action_type == "walk"
                and not WalkingPlace.objects.filter(name=action_detail).exists()
            ):
                if action_detail:
                    WalkingPlace.objects.create(name=action_detail)
                else:
                    print("WalkingPlace action_detail is empty or invalid")

            elif action_type == "wash":
                if action_detail:
                    # 만약 wash 행동에 대한 별도의 모델이 있다면, 여기서 처리합니다.
                    # 예를 들어, WashingPlace.objects.create(name=action_detail) 등
                    print(
                        f"Wash action detail: {action_detail}, completed: {action_completed}"
                    )
                else:
                    print("Wash action_detail is empty or invalid")

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
    permission_classes = []

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
            serializer.save(
                character=character, user=self.request.user, date=timezone.now().date()
            )
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
        character.ended = True
        character.active = False
        character.save()

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
                "records": {
                    "cleaning": "",
                    "exercise": "",
                    "shower": {"completed": False},
                },
                "diary": "",
            }

            for entry in journal_entries.filter(date=date):
                if entry.action_type == "eat":
                    if entry.meal_time:
                        day_data["meals"][entry.meal_time] = entry.action_detail
                elif entry.action_type == "cleaning":
                    day_data["records"]["cleaning"] = entry.action_detail
                elif entry.action_type == "walk":
                    day_data["records"]["exercise"] = entry.action_detail
                elif entry.action_type == "wash":
                    day_data["records"]["shower"] = {
                        "completed": entry.completed,
                    }

            for diary in diary_entries.filter(date=date):
                diary_entry = diary_entries.first()
                day_data["diary"] = diary.diary_text
                day_data["weather"] = diary.weather

            data.append(day_data)

        return Response(data)


# 기록장에서 날짜 클릭했을때 상세정보
class CharacterJournalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, date):
        if request.user.id != int(user_id):
            return Response(
                {"error": "You do not have permission to view this journal."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 날짜 형식 변환
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        journal_entries = JournalEntry.objects.filter(
            character__user_id=user_id, date=date_obj
        )
        # character__user_id와 date로 필터링
        diary_entries = DiaryEntry.objects.filter(
            character__user_id=user_id, date=date_obj
        )

        day_data = {
            "date": date,
            "day": date_obj.strftime("%A"),  # 요일을 날짜로부터 계산
            "weather": "",  # 날씨는 사용자가 입력하도록 설계해야 함
            "meals": {"breakfast": "", "lunch": "", "dinner": "", "snack": ""},
            "records": {"cleaning": "", "exercise": "", "shower": ""},
            "diary": "",
        }

        for entry in journal_entries:
            if entry.action_type == "eat":
                if entry.meal_time:
                    day_data["meals"][entry.meal_time] = entry.action_detail
            elif entry.action_type == "cleaning":
                day_data["records"]["cleaning"] = entry.action_detail
            elif entry.action_type == "walk":
                day_data["records"]["exercise"] = entry.action_detail
            elif entry.action_type == "wash":
                day_data["records"]["shower"] = {
                    "completed": entry.completed,
                }

        if diary_entries.exists():
            diary_entry = diary_entries.first()
            day_data["weather"] = diary_entry.weather
            day_data["diary"] = diary_entry.diary_text

        # 디버깅 메시지 추가
        print(f"Date: {date_obj}")
        print(f"Journal Entries: {journal_entries}")
        print(f"Diary Entries: {diary_entries}")

        return Response(day_data, status=status.HTTP_200_OK)


class RandomRecommendationView(APIView):
    def get(self, request, *args, **kwargs):
        food_recommendations = list(Food.objects.all().values_list("name", flat=True))
        cleaning_recommendations = list(
            CleaningSpot.objects.all().values_list("name", flat=True)
        )
        walking_recommendations = list(
            WalkingPlace.objects.all().values_list("name", flat=True)
        )

        random_foods = random.sample(
            food_recommendations, min(3, len(food_recommendations))
        )
        random_cleanings = random.sample(
            cleaning_recommendations, min(3, len(cleaning_recommendations))
        )
        random_walkings = random.sample(
            walking_recommendations, min(3, len(walking_recommendations))
        )

        return Response(
            {
                "foods": random_foods,
                "cleaning_spots": random_cleanings,
                "walking_places": random_walkings,
            }
        )


class KeywordRecommendationView(APIView):
    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", "")
        keyword = unquote(keyword).strip()  # URL 디코딩 후 공백 제거

        if not keyword:
            return self.get_random_recommendations()

        food_recommendations = list(
            Food.objects.filter(name__icontains=keyword).values_list("name", flat=True)
        )
        cleaning_recommendations = list(
            CleaningSpot.objects.filter(name__icontains=keyword).values_list(
                "name", flat=True
            )
        )
        walking_recommendations = list(
            WalkingPlace.objects.filter(name__icontains=keyword).values_list(
                "name", flat=True
            )
        )

        return Response(
            {
                "foods": food_recommendations,
                "cleaning_spots": cleaning_recommendations,
                "walking_places": walking_recommendations,
            }
        )

    def get_random_recommendations(self):
        food_recommendations = list(Food.objects.all().values_list("name", flat=True))
        cleaning_recommendations = list(
            CleaningSpot.objects.all().values_list("name", flat=True)
        )
        walking_recommendations = list(
            WalkingPlace.objects.all().values_list("name", flat=True)
        )

        random_foods = random.sample(
            food_recommendations, min(3, len(food_recommendations))
        )
        random_cleanings = random.sample(
            cleaning_recommendations, min(3, len(cleaning_recommendations))
        )
        random_walkings = random.sample(
            walking_recommendations, min(3, len(walking_recommendations))
        )

        return Response(
            {
                "foods": random_foods,
                "cleaning_spots": random_cleanings,
                "walking_places": random_walkings,
            }
        )


class UserActivityDatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 다이어리와 행동 기록 조회
        diary_entries = DiaryEntry.objects.filter(user=user).values_list(
            "date", flat=True
        )
        journal_entries = JournalEntry.objects.filter(character__user=user).values_list(
            "date", flat=True
        )

        # 중복되지 않는 날짜 목록 생성
        dates = set(diary_entries) | set(journal_entries)

        # 날짜 목록을 정렬
        sorted_dates = sorted(dates)

        return Response(sorted_dates)
