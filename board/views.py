from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from character.models import JournalEntry, Character
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from konlpy.tag import Okt
import random
from collections import Counter
from .models import EveryList, LifeList
from .serializers import EveryListSerializer, LifeListSerializer

# 한글 불용어 목록
KOREAN_STOPWORDS = [
    '야', '이', '그', '저', '것', '수', '때', '등', '들', '및', '와', '과', '하지만', '또한', '그리고', '그래서', '오늘', '은', '오', '한다', '했다', '있다', '없다', '을', '는', '이', '가'
]

# 동사형 어미 목록
VERB_SUFFIXES = ['하다', '되다', '하다', '싶다', '보다', '있다', '없다', '가다', '오다', '보다', '먹다', '만나다', '주다', '받다', '알다', '모르다', '말하다', '듣다', '걷다', '놀다', '일어나다', '앉다', '서다','겼다']

# 샘플 할 일 추천 데이터
TODO_RECOMMENDATIONS = {
    '먹기': [
        '아침 먹기', '점심 먹기', '저녁 먹기', '간식 먹기', '과일 먹기', '야채 먹기', '샐러드 먹기', 
        '파스타 먹기', '스시 먹기', '한식 먹기', '양식 먹기', '중식 먹기', '디저트 먹기', 
        '아이스크림 먹기', '치킨 먹기', '피자 먹기', '햄버거 먹기', '해산물 먹기', '국수 먹기',
        '라면 먹기', '김밥 먹기', '떡볶이 먹기', '커피 마시기', '차 마시기', '스무디 마시기',
        '샌드위치 먹기', '버거킹 먹기', '맥도날드 먹기', '케이크 먹기', '쿠키 먹기', '와플 먹기',
        '스테이크 먹기', '치즈 먹기', '소시지 먹기', '프라이드 치킨 먹기', '스프 먹기',
        '초밥 먹기', '돈까스 먹기', '비빔밥 먹기', '냉면 먹기', '쌀국수 먹기', '우동 먹기',
        '타코 먹기', '부리토 먹기', '피타 샌드위치 먹기', '팔라펠 먹기', '후무스 먹기',
        '스콘 먹기', '마카롱 먹기', '베이글 먹기', '크루아상 먹기', '페이스트리 먹기',
        '초콜릿 먹기', '젤리 먹기', '푸딩 먹기', '파이 먹기', '타르트 먹기', '블루베리 먹기',
        '라즈베리 먹기', '딸기 먹기', '망고 먹기', '파인애플 먹기', '코코넛 먹기', '참외 먹기',
        '수박 먹기', '포도 먹기', '멜론 먹기', '사과 먹기', '바나나 먹기', '오렌지 먹기',
        '자몽 먹기', '키위 먹기', '파파야 먹기', '두리안 먹기', '드래곤 프루트 먹기', '패션 프루트 먹기',
        '아보카도 먹기', '블랙베리 먹기', '커스터드 애플 먹기', '잭프루트 먹기', '스위트 콘 먹기'
    ],
    '씻기': [
        '손 씻기', '얼굴 씻기', '발 씻기', '목욕하기', '세수하기', '샤워하기', '양치질하기', 
        '머리 감기', '발 닦기', '비누로 손 씻기', '클렌징하기', '핸드워시 사용하기', '스크럽하기',
        '손톱 정리하기', '발톱 정리하기', '마스크팩 하기', '스킨케어 하기', '몸 씻기', '샤워 후 보습제 바르기',
        '헤어 오일 바르기', '립밤 바르기', '면도하기', '발 스크럽 하기', '허브 바스 사용하기'
    ],
    '산책하기': [
        '공원 산책', '강변 산책', '도시 산책', '산책로 걷기', '해변 산책', '저녁 산책', '아침 산책', 
        '숲 산책', '산책하며 사진 찍기', '산책하며 음악 듣기', '산책하며 명상하기', '산책하며 책 읽기',
        '친구와 산책하기', '애완동물과 산책하기', '산책하며 꽃 구경하기', '산책하며 새소리 듣기', '자연 관찰하기',
        '역사적인 장소 산책하기', '조깅하기', '자전거 타기', '스쿠터 타기', '도심 걷기', '트래킹 하기'
    ],
    '샤워하기': [
        '아침 샤워', '저녁 샤워', '운동 후 샤워', '샴푸하기', '바디 워시 사용하기', '따뜻한 물로 샤워', 
        '차가운 물로 샤워', '샤워하며 노래 부르기', '헤어 트리트먼트 사용하기', '바디 스크럽하기', '발 마사지하기',
        '아로마 오일 샤워하기', '거품 목욕하기', '샤워 후 스트레칭 하기', '머리 마사지하기', '샤워 캡 사용하기',
        '향 좋은 샴푸 사용하기', '발바닥 마사지하기', '샤워 후 로션 바르기', '헤어팩 사용하기', '샤워 젤 사용하기'
    ],
    '기본추천': [
        '책 읽기', '명상하기', '음악 듣기', '친구와 대화하기', '스트레칭하기', '요가하기', 
        '영화 감상하기', '자전거 타기', '여행 계획 세우기', '새로운 취미 시작하기', 
        '자원 봉사 활동 참여하기', '정원 가꾸기', '퍼즐 맞추기', '악기 연주 배우기', 
        '새로운 레시피 요리하기', '미술 작품 감상하기', '온라인 강의 듣기', '긍정적인 일기 쓰기',
        '마라톤 준비하기', '사진 찍기', '춤추기', '박물관 방문하기', '산책로 탐험하기', '캠핑 준비하기',
        '조깅하기', '명상 음악 듣기', '플라워 어레인지먼트 배우기', '비디오 게임 하기', 'DIY 프로젝트 하기',
        '베이킹 하기', '지역 행사 참여하기', '드라이브하기', '스케이트 타기', '스노클링하기', '등산하기',
        '야외 피크닉 하기', '도서관 가기', '칼리그래피 배우기', '친구들과 게임하기', '새로운 언어 배우기',
        '낚시하기', '드로잉 하기', '클래식 음악 듣기', '마음 챙김 운동 하기', '다큐멘터리 보기', '도예 배우기',
        '낮잠 자기', '명상 책 읽기', '자전거 수리하기', '뜨개질 배우기', '조리 도구 정리하기',
        '아침 일기 쓰기', '전시회 관람하기', '셀프 마사지 배우기', '허브차 만들기', '음악 연주하기',
        '아로마 테라피 즐기기', '공예 배우기', '천체 관측하기', '집 청소하기', '중고물품 기부하기',
        '자연 산책하기', '동네 산책하기', '재즈 음악 듣기', '요리 책 읽기', '식물 가꾸기', '공예품 만들기',
        '기타 배우기', '플룻 연주 배우기', '자수 배우기', '애완동물 돌보기', '사회적 활동 참여하기',
        '새로운 운동 시작하기', '해변 가기', '패들 보트 타기', '자연 사진 찍기', '명상 앱 사용하기',
        '건강식 요리하기', '야간 산책하기', '시집 읽기', '보드 게임 하기', '비디오 블로그 시작하기',
        '반려동물 훈련하기', '스케이트보드 타기', '스탠드업 코미디 보기', '주말 여행 계획하기', '자전거 여행 하기',
        '도시 탐험하기', '낙서 하기', '정원에서 독서하기', '반려 식물 돌보기', '타로 카드 공부하기',
        '자연 다큐멘터리 보기', '심리학 책 읽기', '새로운 도시 방문하기', '자기 계발 서적 읽기', '수영 배우기'
    ]
}


class RecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        character_id = data.get('character_id')
        if not character_id:
            return JsonResponse({"error": "character_id field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 캐릭터와 연관된 JournalEntry 데이터를 가져오기
        journal_entries = JournalEntry.objects.filter(character_id=character_id)
        recommendations = self.generate_recommendations(journal_entries)
        return JsonResponse({"recommendations": recommendations}, status=status.HTTP_200_OK)

    def generate_recommendations(self, journal_entries):
        # 모든 일기 내용을 합침
        combined_content = ' '.join(entry.action_detail for entry in journal_entries if entry.action_detail)
        
        okt = Okt()
        tokens = okt.morphs(combined_content)
        filtered_tokens = [word for word in tokens if word not in KOREAN_STOPWORDS and len(word) > 1]

        word_freq = Counter(filtered_tokens)
        most_common_words = [word for word, _ in word_freq.most_common(3)]

        recommendations = []
        for word in most_common_words:
            if word in TODO_RECOMMENDATIONS:
                recommendations.extend(random.sample(TODO_RECOMMENDATIONS[word], min(len(TODO_RECOMMENDATIONS[word]), 3)))
        
        # 기본 추천 추가
        recommendations.extend(random.sample(TODO_RECOMMENDATIONS['기본추천'], 3))

        # 중복 제거 후 추천 리스트 생성
        existing_actions = set(entry.action_detail for entry in journal_entries if entry.action_detail)
        unique_recommendations = [rec for rec in recommendations if rec not in existing_actions]

        # 추천 목록을 10개 이하로 제한
        random.shuffle(unique_recommendations)
        return unique_recommendations[:10]


@csrf_protect
def recommend_page(request):
    return render(request, 'recommend.html')


class EveryListView(generics.ListCreateAPIView):
    queryset = EveryList.objects.all()
    serializer_class = EveryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EveryList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EveryListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EveryList.objects.all()
    serializer_class = EveryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EveryList.objects.filter(user=self.request.user)

class LifeListView(generics.ListCreateAPIView):
    queryset = LifeList.objects.all()
    serializer_class = LifeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LifeList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LifeListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LifeList.objects.all()
    serializer_class = LifeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LifeList.objects.filter(user=self.request.user)