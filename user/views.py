from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser
from .serializers import ProfileSerializer, CustomUserSerializer, CheckUserIDSerializer
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken


class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "회원가입 성공"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "회원가입 실패", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 아이디 중복 검사
class CheckUserIDView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = CheckUserIDSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            exists = CustomUser.objects.filter(user_id=user_id).exists()
            return Response({"user_id_exists": exists}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        password = request.data.get("password")
        user = authenticate(request, user_id=user_id, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "로그인 성공",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED
            )


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)


# 계정탈퇴
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        logout(request)
        return Response({"message": "계정 삭제 성공"}, status=status.HTTP_200_OK)


# 북마크한 글 보기
class BookmarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 북마크한 글을 불러오는 로직 구현
        return Response({"message": "북마크한 글 목록"}, status=status.HTTP_200_OK)


# 마이페이지
class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 마이페이지 로직 구현
        return Response({"message": "마이페이지"}, status=status.HTTP_200_OK)


# 비밀번호 재설정을 위한 이메일 확인
class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        associated_user = CustomUser.objects.filter(email=email).first()
        if associated_user:
            return Response({"email": email}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "해당 이메일 주소가 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )


# 비밀번호 재설정
class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        new_password1 = request.data.get("new_password1")
        new_password2 = request.data.get("new_password2")
        if new_password1 != new_password2:
            return Response(
                {"error": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        associated_user = CustomUser.objects.filter(email=email).first()
        if associated_user:
            associated_user.set_password(new_password1)
            associated_user.save()
            return Response(
                {"message": "비밀번호 재설정 성공"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "해당 이메일 주소가 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )


# 프로필 사진 수정
class ProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        photo = request.FILES.get("photo")
        username = request.data.get("username")

        if photo:
            user.photo = photo

        if username:
            user.username = username

        if photo or username:
            user.save()
            return Response(
                {"message": "프로필이 성공적으로 수정되었습니다."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "수정할 정보가 제공되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# 개인 정보 수정
class PersonalInfoEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )  # 파일 업로드와 폼 데이터를 위해 파서 추가

    def post(self, request, *args, **kwargs):
        user = request.user
        user_id = request.data.get("user_id")
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        # 비밀번호 확인
        if password and password != password2:
            return Response(
                {"error": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # user_id 중복 확인
        if (
            user_id
            and CustomUser.objects.filter(user_id=user_id).exclude(pk=user.pk).exists()
        ):
            return Response(
                {"error": "이미 존재하는 ID입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 필드별 업데이트
        if user_id:
            user.user_id = user_id
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return Response(
                {"message": "비밀번호가 변경되었습니다. 다시 로그인 해주세요."},
                status=status.HTTP_200_OK,
            )

        user.save()
        return Response(
            {"message": "프로필이 성공적으로 수정되었습니다."},
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)
