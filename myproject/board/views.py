import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from post.models import Post  
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from konlpy.tag import Okt
import nltk
from collections import Counter


# 한글 불용어 목록
KOREAN_STOPWORDS = [
    '야', '이', '그', '저', '것', '수', '때', '등', '들', '및', '와', '과', '하지만', '또한', '그리고', '그래서', '오늘', '은', '오', '한다', '했다', '있다', '없다', '을', '는', '이', '가'
]

# 동사형 어미 목록
VERB_SUFFIXES = ['하다', '되다', '하다', '싶다', '보다', '있다', '없다', '가다', '오다', '보다', '먹다', '만나다', '주다', '받다', '알다', '모르다', '말하다', '듣다', '걷다', '놀다', '일어나다', '앉다', '서다','겼다']


# 샘플 할 일 추천 데이터
TODO_RECOMMENDATIONS = {
    '영화': ['영화 보기', '영화 리뷰 쓰기', '영화 예매하기', '영화 토론하기', '영화 촬영하기', '영화 편집하기'],
    '영화관': ['영화관 가기', '영화관에서 영화 보기', '영화관 예매하기'],
    '영화제': ['영화제 참석하기', '영화제 정보 찾기', '영화제 리뷰 쓰기'],
    '드라마': ['드라마 보기', '드라마 리뷰 쓰기', '드라마 추천 받기', '드라마 예고편 보기'],
    '연극': ['연극 보기', '연극 예매하기', '연극 리뷰 쓰기'],
    '공연': ['공연 보기', '공연 예매하기', '공연 리뷰 쓰기'],
    '책': ['책 읽기', '책 리뷰 쓰기', '책 추천 받기', '책 예매하기'],
    '음악': ['음악 듣기', '음악 리뷰 쓰기', '음악 추천 받기', '콘서트 예매하기'],
    '게임': ['게임 하기', '게임 리뷰 쓰기', '게임 정보 찾기', '게임 추천 받기'],
    '쇼핑': ['쇼핑하기', '쇼핑 목록 작성하기', '쇼핑 정보 찾기', '쇼핑 리뷰 쓰기'],
    '운동': ['조깅하기', '헬스장 가기', '요가하기', '자전거 타기', '수영하기', '등산하기', '축구하기', '농구하기', '테니스 치기'],
    '공부': ['독서하기', '온라인 강의 듣기', '복습하기', '예습하기', '문제 풀기', '스터디 그룹 참여하기'],
    '여행': ['여행 계획 세우기', '여행지 검색하기', '여행 가방 싸기', '여행 사진 찍기', '여행 블로그 쓰기'],
    '산책': ['공원에서 산책하기', '강변에서 산책하기', '산책 코스 탐색하기', '산책 중 명상하기'],
    '기분': ['명상하기', '기분 전환할 만한 영화 보기', '기분 좋은 음악 듣기', '기분 좋은 책 읽기', '기분 좋은 친구 만나기'],
    '별로야': ['기분 전환을 위한 영화 보기', '새로운 취미 찾기', '즐거운 활동 계획하기'],
    '야구': ['야구 경기 관람하기', '야구 시합 참여하기', '야구 연습하기', '야구 관련 뉴스 읽기'],
    '경기': ['스포츠 경기 보기', '스포츠 경기 분석하기', '스포츠 경기 예측하기', '스포츠 경기 참여하기'],
    '보러': ['공연 보러 가기', '전시회 보러 가기', '영화 보러 가기', '드라마 보러 가기'],
    '운동': ['조깅하기', '헬스장 가기', '요가하기', '자전거 타기', '수영하기', '등산하기', '축구하기', '농구하기', '테니스 치기'],
    '공부': ['독서하기', '온라인 강의 듣기', '복습하기', '예습하기', '문제 풀기', '스터디 그룹 참여하기'],
    '여행': ['여행 계획 세우기', '여행지 검색하기', '여행 가방 싸기', '여행 사진 찍기', '여행 블로그 쓰기'],
    '산책': ['공원에서 산책하기', '강변에서 산책하기', '산책 코스 탐색하기', '산책 중 명상하기'],
    '기분': ['명상하기', '기분 전환할 만한 영화 보기', '기분 좋은 음악 듣기', '기분 좋은 책 읽기', '기분 좋은 친구 만나기'],
    '별로야': ['기분 전환을 위한 영화 보기', '새로운 취미 찾기', '즐거운 활동 계획하기'],
    
}

class RecommendView(APIView):

    def post(self, request):
        data = request.data

        print("Received data:", data)  # 요청 데이터 로그 출력

        post_ids = data.get('post_ids', [])
        print("post_ids:", post_ids)
        if not post_ids:
            print("No post_ids provided")
            return JsonResponse({"error": "post_ids field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # post_ids로부터 Post 객체들 가져오기
        posts = Post.objects.filter(id__in=post_ids)
        print("Fetched posts:", posts)

        if not posts.exists():
            print("No valid posts found for provided post_ids:", post_ids)
            return JsonResponse({"error": "No valid posts found"}, status=status.HTTP_400_BAD_REQUEST)

        recommendations = self.generate_recommendations(posts)
        return JsonResponse({"recommendations": recommendations}, status=status.HTTP_200_OK)

    def generate_recommendations(self, posts):
        # 모든 일기 내용을 합침
        combined_content = ' '.join(post.content for post in posts)
        
        # 패턴 인식
        patterns = re.findall(r'(\w+)\s*(좋|고\s*싶다)', combined_content)
        patterns = [pattern[0] for pattern in patterns]  # 패턴에서 단어만 추출
        print("Patterns found:", patterns)  # 패턴 로그 출력
        
        # 토큰화 및 불용어 제거
        okt = Okt()
        tokens = okt.morphs(combined_content)
        print("Tokens:", tokens)  # 토큰 로그 출력
        filtered_tokens = [word for word in tokens if word not in KOREAN_STOPWORDS and len(word) > 1]
        print("Filtered tokens:", filtered_tokens)  # 필터된 토큰 로그 출력

        # 가장 빈도 높은 단어 찾기
        word_freq = Counter(filtered_tokens)
        most_common_words = [word for word, _ in word_freq.most_common(3)]
        print("Most common words:", most_common_words)  # 빈도 높은 단어 로그 출력
        
        # 키워드 기반 추천
        recommendations = []
        for word in most_common_words + patterns:
            if word in TODO_RECOMMENDATIONS:
                recommendations.extend(TODO_RECOMMENDATIONS[word])
        print("Recommendations:", recommendations)  # 추천 결과 로그 출력

        return recommendations

@csrf_protect
def recommend_page(request):
    return render(request, 'recommend.html')