from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Character, Diary
from .serializers import CharacterSerializer, DiarySerializer, ActionSerializer
from django.shortcuts import get_object_or_404


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class ActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, character_id):
        character = get_object_or_404(Character, id=character_id, user=request.user)
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data["action_type"]
            detail = serializer.validated_data["detail"]
            character.current_action = f"{action}: {detail}"
            character.gauge += 5
            character.save()
            if character.gauge >= 100:
                return Response({"message": "Gauge is full"}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinalizeActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, character_id):
        character = get_object_or_404(Character, id=character_id, user=request.user)
        final_action = request.data.get("final_action")
        if final_action:
            character.final_action = final_action
            character.save()
            character.delete()  # 캐릭터 삭제
            return Response(
                {"message": "Character finalized and deleted"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Final action not provided"}, status=status.HTTP_400_BAD_REQUEST
        )


class DiaryEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DiarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
