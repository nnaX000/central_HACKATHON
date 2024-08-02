from rest_framework import serializers
from .models import CustomUser, Profile
import json


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["age"]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    photo_url = serializers.SerializerMethodField()  # 추가된 부분

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "user_id",
            "username",
            "email",
            "password",
            "photo_url",
            "profile",
        ]  # photo_url 필드를 추가
        extra_kwargs = {"password": {"write_only": True}}

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and hasattr(obj.photo, "url"):
            return request.build_absolute_uri("/myproject" + obj.photo.url)
        return None

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        if isinstance(profile_data, str):  # JSON 문자열로 전달된 경우
            profile_data = json.loads(profile_data)

        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        if isinstance(profile_data, str):  # JSON 문자열로 전달된 경우
            profile_data = json.loads(profile_data)

        password = validated_data.pop("password", None)

        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.photo = validated_data.get("photo", instance.photo)

        if password:
            instance.set_password(password)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.age = profile_data.get("age", profile.age)
            profile.save()

        return instance


class CheckUserIDSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
