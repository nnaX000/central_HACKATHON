| 엔드포인트 | 위치 | 작업상세 | 데이터송수신유형 | 데이터 형태 |  |
| --- | --- | --- | --- | --- | --- |
| home/ | 홈 | 홈화면 띄우기 | POST |  |  |
| X | 리스트 모아보기 | 에브리리스트와 라이프 리스트를 한번에 불러옴 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"everylist": [
{
"id": 1,
"user": 1,
"task": "책 읽기",
"due_date": "2024-07-25",
"due_time": "14:00:00",
"completed": false,
"created_at": "2024-07-20T14:00:00Z",
"updated_at": "2024-07-20T14:00:00Z"
},
{
"id": 2,
"user": 1,
"task": "명상하기",
"due_date": "2024-07-25",
"due_time": "15:00:00",
"completed": false,
"created_at": "2024-07-20T15:00:00Z",
"updated_at": "2024-07-20T15:00:00Z"
}
],
"lifelist": [
{
"id": 1,
"user": 1,
"goal": "여행 계획 세우기",
"description": "유럽 여행 계획 세우기",
"target_date": "2024-07-25",
"target_time": "16:00:00",
"completed": false,
"created_at": "2024-07-20T16:00:00Z",
"updated_at": "2024-07-20T16:00:00Z"
},
{
"id": 2,
"user": 1,
"goal": "새로운 취미 시작하기",
"description": "요가 배우기",
"target_date": "2024-07-25",
"target_time": "17:00:00",
"completed": false,
"created_at": "2024-07-20T17:00:00Z",
"updated_at": "2024-07-20T17:00:00Z"
}
]
}

실패시
401 Unauthorized: 인증되지 않은 사용자
403 FORBIDDEN : 접근 권한이 없는 사용자 |  |
| notifications/ | 알람 | - 현재 사용자의 모든 알림을 조회, 알림은 최신 순으로 정렬되어 반환됨
- read 변수는 알림(Notification)이 사용자가 읽었는지 여부를 나타내는 역할. 이 변수는 Boolean 타입으로 설정되며, 기본값은 False, 사용자가 알림을 읽으면 이 값을 True로 변경 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
[
{
"id": 1,
"user": 1,
"post": 5,
"message": "user1님이 'Post Title' 글을 좋아합니다.",
"created_at": "2024-07-24T12:34:56Z",
"read": false
},
{
"id": 2,
"user": 1,
"post": 3,
"message": "user2님이 'Another Post' 글을 좋아합니다.",
"created_at": "2024-07-24T13:45:12Z",
"read": true
}
] |  |
| /notifications/mark_as_read/int:pk/ | 알림을 읽음 상태로 변 | 사용자가 자신의 알림을 읽음 상태로 변경할 수 있음 | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Content-Type: application/json
Authorization: Bearer <access_token>

- 성공시
200 ok
{
"message": "Notification marked as read"
}
- 실패시
404 not found
{
"detail": "Not found."
}
401 Unauthorized
{
"detail": "Authentication credentials were not provided."
}
403 Forbidden
{
"detail": "You do not have permission to perform this action."
} |  |
| signup/ | 회원가입 | 회원가입 | POST | 1. Body : <form-data>
user_id : 아이디[Text]
username : 이름[Text]
password : 비밀번호[Text]
email : 이메일[Text]
photo : 사진[첨부파일]

- 성공시
201 create
{”message” : “회원가입 성공”} |  |
| check_user_id/ | 회원가입 | 아이디중복검사 | POST | 1. Body : <form-data>
user_id : 아이디[Text]

- 성공시
200 ok
{
"user_id_exists": True. 
}
—> 중복있음(=아이디 다른걸로 바꿔야함)
—————————————
{
"user_id_exists": false 
}
—> 중복없음 |  |
| login/

 | 로그인 | 로그인 | POST | 1.  Body : <form-data>
user_id : 아이디[Text]
password : 비밀번호[Text]

- 성공시
200 ok
{”messege”: “로그인 성공”,
”refresh”: “대충 엄청 긴 문자열”,
”access”:”대충 엄청 긴 문자열”} |  |
| delete-account/ | 마이페이지 | 계정 삭제 | DELETE | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

- 성공시
200 ok
{”messege”: “계정 삭제 성공”} |  |
| logout/ | 마이페이지 | 로그아웃 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

- 성공시
200 ok
{”messege”: “로그아웃 성공”} |  |
| profile-edit/ | 마이페이지 | 프로필 “사진 및 닉네임” 변경 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : <form-data>
username : 닉네임[Text]
photo: 사진[첨부파일]

- 성공시
200 ok
{"message": "프로필이 성공적으로 수정되었습니다.”} |  |
| personal-info-edit/ | 마이페이지 | 프로필 “정보” 수정 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : <form-data>
user_id : 아이디[Text]
username : 이름[Text]
password : 비밀번호[Text]
password2 : 비밀번호 확인[Text]
email : 이메일[Text]

- 성공시
200 ok
{”messege”: “프로필이 성공적으로 수정되었습니다.”} |  |
| password-reset-request/ | 비밀번호 찾기 | 비밀번호 변경을 위한 일치하는 이메일 찾기 | POST | 2.  Body : raw(json)
{
"email": "mailto:20211307@sungshin.ac.kr"
}

- 성공시
200 ok
{
"email": "mailto:20221307@sungshin.ac.kr"
}

일치하는 이메일이 없을시
404 not found
{
"error": "해당 이메일 주소가 없습니다."
} |  |
| password-reset-confirm/ | 비밀번호 찾기 | 비밀번호 변경하기 | POST | 2.  Body : raw(json)
{
"email": "mailto:20221307@sungshin.ac.kr",
"new_password1": "3333",
"new_password2": "3333"
}

- 성공시
200 ok
{
"message": "비밀번호 재설정 성공"
}

일치하는 이메일이 없을시
404 not found
{
"error": "해당 이메일 주소가 없습니다."
} |  |
| http://127.0.0.1:8000/user/detail/ | 사용자 정보 필요한 곳 어디에서나..
예) 마이페이지에서 회원이름 띄워야 할때 | 사용자 정보(id,user_id, username, email,photo경로 다 반환해줌. 선택적으로 쓰면 됨)

★ 프로필사진을 불러올때는 photo_url에 대해서 get요청을 보내면 받아볼 수 있음.(Header와 body 공란)

 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

- 성공시
200 ok

{
    "id": 6,
    "user_id": "kkkknnnn",
    "username": "포포",
    "email": "34527865@naver.com",
    "photo_url": "http://3.25.237.92:8000/myproject/media/default-profile_mo6qkr1.jpg",
    "profile": {
        "age": null
    }
} |  |
| 캐릭터 필드명은 다음과 같이 지정했습니다 —> | parrot 
dolphin
squirrel |  |  |  |  |
| characters/ | 캐릭터 만들기 | 캐릭터 생성 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : raw(json)
{
    "name": "My Parrot", //캐릭터 이름
    "type": "parrot" //캐릭터 종류
}

- 성공시
201 created
{
   "id": 3,
   "user": 3,
   "name": "My Parrotd",
   "type": "parrot",
   "gauge": 0,
   "active": true
} |  |
| characters/ | 캐릭터 만들기 | 캐릭터 정보 가져오기
★ 현재 사용자가 사용중인 캐릭터 정보만 나옴.
엔딩보기 한 캐릭터는 안나옴. | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

- 성공시
200 ok
[
 {
   "id": 1,
   "user": 1,
   "name": "my parrot",
   "type": "parrot",
   "gauge": 0,
   "active": true
  }
]

 |  |
| characters/<character_id>/ | 캐릭터 만들기 | 캐릭터 종류 바꾸기 | PATCH | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : raw(json)
{
"type": "dolphin"
}

- 성공시
200 ok
{
  "id": 1,
  "user": 1,
  "name": "my parrot",
  "type": "dolphin",
  "gauge": 0,
  "active": true
} |  |
| journal_entries/ | 캐릭터 키우기 | 캐릭터 행동하기 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : raw(json)
- <밥 먹기>
{
   "character": 1,  //  캐릭터 ID
   "action_type": "eat",
   "meal_time": "breakfast",  // "breakfast", "lunch", "dinner", "snack" 중 선택
   "action_detail": "시리얼과 우유", //뭘 먹었는지
 "completed": true  // 예: True 아니오: False
}
성공시
201 created
{
   "id": 2,
   "character": 1,
   "date": "2024-07-23",
   "action_type": "eat",
   "meal_time": "breakfast",
   "action_detail": "시리얼과 우유", 
   "completed": false
}
- <씻기>
{
   "character": 1,  // 캐릭터 ID
   "action_type": "wash",
   "completed": true  // 예: True 아니오: False
}
성공시
201 created
{
   "id": 3,
   "character": 1,
   "date": "2024-07-23",
   "action_type": "wash",
   "meal_time": null,
   "action_detail": null,
   "completed": true
}
- <운동하기>
{
   "character": 1,   // 캐릭터 ID
   "action_type": "walk",
   "action_detail": "배드민턴", //뭔 운동했는지
   "completed": true
}
성공시
201 created
{
   "id": 7,
   "character": 1,  
   "date": "2024-07-23",
   "action_type": "walk",
   "meal_time": null,
   "action_detail": "베란다",
   "completed": true
}

- 청소하기
{
   "character": 1,  // 캐릭터 ID
   "action_type": "cleaning",
   "action_detail": "방", //어딜 청소했는지
   "completed": true
}

성공시
201 created
{
   "id": 8,
   "character": 1,
   "date": "2024-07-23",
   "action_type": "clean",
   "meal_time": null,
   "action_detail": "방",
   "completed": true
} |  |
| characters/<character_id>/records/<date>/

ex)
characters/1/records/2024-08-05/ | 캐릭터 키우기 - 행동하기 | 일별로 이미 저장해둔 먹기 기록 반환 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
{
"date": "2024-08-05",
"day": "Monday",
"meals": {
"breakfast": [
"시리얼과 우유"
],
"lunch": [
"콩나물국밥",
"토스트"
],
"dinner": [
"순두부찌개",
"밥",
"스테이크"
],
"snack": [
"젤리",
"우유",
"빵"
]
}
} |  |
| http://127.0.0.1:8000/recommendations/random/ | 캐릭터 키우기 - 행동하기 | 랜덤 추천기능 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
{
"foods": [
"아이스크림빙수",
"해물전",
"부추전"
],
"cleaning_spots": [
"주방 서랍",
"차고",
"재활용품 정리함"
],
"walking_places": [
"서핑",
"자이로토닉",
"골프"
]
} |  |
| http://127.0.0.1:8000/recommendations/keyword/?keyword=%EC%9E%90’사용자가 입력한 키워드’

예시 ) http://127.0.0.1:8000/recommendations/keyword/?keyword=%EC%A7%80조 | 캐릭터 키우기 - 행동하기 | 사용자가 치는 텍스트에 따라 추천해주기 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok

{
"foods": [
"장조림",
"연근조림",
"조개탕",
"조개구이",
"조기매운탕",
"코다리조림",
"조기구이",
"우엉조림",
"연근조림",
"조개탕",
"조개구이",
"조기매운탕",
"코다리조림",
"조기구이",
"우엉조림",
"고등어조림",
"연근조림"
],
"cleaning_spots": [],
"walking_places": [
"조깅",
"체조"
]
}
 |  |
| http://127.0.0.1:8000/characters/gauge/ | 캐릭터 키우기 | 캐릭터 게이지 조회하기 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
{
   "gauge": 40
} |  |
| user-activity-dates/ | 기록장 | 기록장 맨 처음 페이지에서 날짜 띄우기 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
[
"2024-07-30"
] |  |
| diary_entries/ | 기록장 | 일기(메모) 쓰기 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

2.  Body : raw(json)
-입력예시
{
   "character": 1, // 캐릭터 아이디
   "weather": "sunny",
   "diary_text": "오늘은 날씨가 좋았다."
}

성공시
201 created
{
   "id": 3,
   "character": 1,
   "date": "2024-07-24",
   "weather": "sunny",
   "diary_text": "오늘은 날씨가 좋았다."
} |  |
| characters/end/ | 엔딩보기- 캐릭터 비활성화 | 캐릭터 비활성화시키기 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
{
"message": "Character has been ended."
} |  |
| characters/<int:character_id>/ending/

ex) characters/1/ending/ | 엔딩보기 - 엔딩리스트 보기 | 엔딩리스트 보기

★ 날짜별로 행동기록, 일기기록 반환
★ 입력 안한 건 그냥 “”로 반환됨 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok

[
{
"date": "2024-08-05",
"day": "Monday",
"weather": "cloudy",
"meals": {
"breakfast": [
"시리얼과 우유",
"빵"
],
"lunch": [
"설렁탕",
"주스",
"껌"
],
"dinner": [
"닭도리탕",
"단무지"
],
"snack": [
"스타벅스 케이크",
"우유",
"사탕",
"젤리"
]
},
"records": {
"cleaning": [],
"exercise": [],
"shower": []
},
"diary": "날씨 배드."
}
] |  |
| characters/<id>/journal/<date>/

예시 : http://127.0.0.1:8000/characters/1/journal/2024-07-25/

★ 여기서 id는 유저 정보 반환했을때 정보 중 하나.
user_id 아니고 그냥 id필드.

 | 기록장 | 특정 날짜 클릭시 그때 행동기록, 일기기록 보기 | GET | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기

성공시
200 ok
{
"date": "2024-07-25",
"day": "Thursday",
"weather": "sunny",
"meals": {
"breakfast": "시리얼과 우유",
"lunch": "요거트",
"dinner": "바게트",
"snack": "뿡"
},
"records": {
"cleaning": "거실",
"exercise": "배드민턴과 탁구",
"shower": {
"completed": false //True: 샤워함 , False : 샤워안함
}
},
"diary": "에어컨이 고장나서 너무 더웠다.."
} |  |
| api/token/ | get JWT token | JWT token 얻기 위한 링크 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
2.  Body : raw(json)
-입력예시
{
  "username": "사용자 이름 (Text)",
  "password": "비밀번호 (Text)"
}
성공시
200 ok
{
"refresh": "리프레시 토큰 (Text)",
"access": "액세스 토큰 (Text)"
}
 |  |
| api/token/refresh/ |  | Refresh JWT token | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
2.  Body : raw(json)
-입력예시
{
"refresh": "리프레시 토큰 (Text)"
}
성공시
200 ok
{
"access": "액세스 토큰 (Text)"
} |  |
| post/create/ | 게시물 생성 |  | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
Body : raw(json)
{
"content": "새로운 게시물 내용",
"image": null
}
2.  응답
성공시
201 CREATED
{
"message": "Post created successfully"
}
실패시
403 FORBIDDEN (작성 금지 상태인 경우)
{
"message": "You are banned from posting until YYYY-MM-DD HH:MM:SS"
} |  |
| post/like/https://www.notion.so/188a03d20ea34e80ab81ca7f4b34261c?pvs=21/ | 게시물 좋아요 |  | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"liked": "좋아요 상태 (true 또는 false)",
"total_likes": "좋아요 총 개수"
} |  |
| post/posthome/ |  |  | GET | 1.요청:
쿼리 파라미터:
sort (선택 사항): 정렬 기준 ('date' 또는 'likes')
category (선택 사항): 게시물 카테고리 ('latest', 'my_posts', 'liked_posts')
2.  응답
성공시
200 ok
[
{
"id": 1,
"content": "This is a sample post",
"image": "http://example.com/media/post_images/sample.jpg",
"date_posted": "2024-08-05T12:34:56Z",
"author_username": "john_doe",
"author_profile": {
"profile_image": "http://example.com/media/profile_images/john_doe.jpg"
},
"likes": [2, 3, 4],
"total_likes": 3
},
{
"id": 2,
"content": "Another sample post",
"image": null,
"date_posted": "2024-08-04T11:22:33Z",
"author_username": "jane_smith",
"author_profile": {
"profile_image": "http://example.com/media/profile_images/jane_smith.jpg"
},
"likes": [1, 2],
"total_likes": 2
}
] |  |
| post/update/<https://www.notion.so/188a03d20ea34e80ab81ca7f4b34261c?pvs=21>/ | 게시물 수정 |  | PATCH | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
Body : raw(json)
{
"title": "제목 (선택 사항)",
"content": "내용 (선택 사항)"
}

2.  응답
성공시
200 ok
{
"message": "게시물 수정 성공"
}
실패시
403 FORBIDDEN
{
"message": "Unauthorized"
}
 |  |
| post/delete/https://www.notion.so/188a03d20ea34e80ab81ca7f4b34261c?pvs=21/ | 게시물 삭제 |  | DELETE | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"message": "게시물 삭제 성공"
}
실패시
403 FORBIDDEN
{
"message": "Unauthorized"
} |  |
| post/int:pk/posts | 사용자 게시물 목록 |  | GET | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
[
{
"id": "게시물 ID",
"title": "제목",
"content": "내용",
"author": "작성자",
"date_posted": "작성일",
"total_likes": "좋아요 수"
},
...
]
 |  |
| post/int:pk/ | 게시물 상세보기 | 게시글을 눌렀을 때의 디테일 페이지 | GET | 1.요청:
X
2.  응답
성공시
200 ok
{
"id": "게시물 ID",
"title": "제목",
"content": "내용",
"author": "작성자",
"date_posted": "작성일",
"total_likes": "좋아요 수"
} |  |
| post/notifications/read/int:pk/ |  | 특정 알림을 읽음 상태로 변경 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"message": "Notification marked as read"
}
실패시
403 FORBIDDEN
{
"message": "Notification not found"
}
404 Not Found
{
"message": "Notification not found"
} |  |
| post/like/int:pk/ |  | - 특정 게시글을 좋아요하거나 좋아요를 취소
- 만약 게시글을 좋아요하면 작성자에게 알림이 생성됨 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"liked": true,
"total_likes": 10
}

200 OK, Unliked
{
"liked": false,
"total_likes": 9
}
실패시
403 FORBIDDEN
{
"message": "Post not found"
}
404 Not Found
{
"message": "Unauthorized"
} |  |
| post/report_post/int:pk/ | 특정 게시물을 신고 | 신고가 10번 이상 접수되면 게시물이 삭제되고 작성자가 일주일 동안 게시물 작성이 금지됨 | POST | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"message": "Post reported successfully"
}
실패시
400 Bad Request (이미 신고한 경우)
{
"message": "You have already reported this post."
}
 |  |
| board/recommend/ | Get Recommendations | 추천목록을 만드는 링크 | post | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  Body : raw(json)
예시)
{
"character_id": 1 //캐릭터 아이디
}
성공시
200 ok
{
"recommendations": "추천 리스트 (Array)"
} |  |
| board/recommend_page/ | 추천 페이지 | 추천 목록을 보여주는 페이지 |  | 1. Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
2.  응답
성공시
200 ok
{
"message": "게시물 삭제 성공"
}
실패시
403 FORBIDDEN
{
"message": "Unauthorized"
} |  |
| board/add_recommendations/ |  | 추천된 항목들을 선택하여 에브리리스트에 추가 | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{
"Authorization": "Bearer Token (액세스 토큰)"
}
Body : raw(json)
{
"recommendations": [
"책 읽기",
"명상하기",
"음악 듣기"
]
}

2.  응답
성공시
200 ok
{
"success": "Recommendations added to your EveryList"
}
 |  |
| board/everylist/ | 에브리리스트
불러오기 | 현재 사용자의 모든 EveryList 항목을 반환 | GET | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>

2.  응답
성공시
200 ok
[
{
"id": 1,
"user": 1,
"task": "Test Task",
"due_date": "2024-07-25",
"due_time": "15:00:00",
"completed": false,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:00:00Z"
},
...
] |  |
| board/everylist/ | 에브리리스트 생성 | 새로운 EveryList 항목을 생성 | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
{Content-Type: application/json
Authorization: Bearer <access_token>
Body : raw(json)
{
"task": "New Task",
"due_date": "2024-07-26",
"due_time": "14:30:00",
"completed": false
}
2.  응답
성공시
201 Created
{
"id": 2,
"user": 1,
"task": "New Task",
"due_date": "2024-07-26",
"due_time": "14:30:00",
"completed": false,
"created_at": "2024-07-25T14:30:00Z",
"updated_at": "2024-07-25T14:30:00Z"
} |  |
| board/everylist/int:pk/ | 보여줌 | 선택한 EveryList 항목을 반환 | GET  | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>
2.  응답
성공시
200 ok
{
"id": 1,
"user": 1,
"task": "Test Task",
"due_date": "2024-07-25",
"due_time": "15:00:00",
"completed": false,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:00:00Z"
} |  |
| board/everylist/int:pk/ | 업데이트 |  EveryList 항목을 업데이트 | PUT | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Content-Type: application/json
Authorization: Bearer <access_token>
Body : raw(json)
{
"task": "Updated Task",
"due_date": "2024-07-27",
"due_time": "16:00:00",
"completed": true
}

2.  응답
성공시
200 ok
{
"id": 1,
"user": 1,
"task": "Updated Task",
"due_date": "2024-07-27",
"due_time": "16:00:00",
"completed": true,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:40:00Z"
} |  |
| board/everylist/int:pk/ | 삭제 | 특정 EveryList 항목을 삭제 | DELETE | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>
2.  응답
성공시
204 No Content |  |
| board/lifelist/ | 라이프리스트 | 현재 사용자의 모든 LifeList 항목을 반환 | GET | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>
2.  응답
성공시
200 ok
[
{
"id": 1,
"user": 1,
"goal": "Test Goal",
"description": "Description of the test goal",
"target_date": "2024-12-31",
"target_time": "23:59:00",
"completed": false,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:00:00Z"
},
...
] |  |
| board/lifelist/ | 라이프리스트 생성 | 새로운 LifeList 항목을 생성 | POST | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Content-Type: application/json
Authorization: Bearer <access_token>
Body : raw(json)
{
"goal": "New Goal",
"description": "Description of the new goal",
"target_date": "2024-12-31",
"target_time": "23:59:00",
"completed": false
}
2.  응답
성공시
201 Created
{
"id": 2,
"user": 1,
"goal": "New Goal",
"description": "Description of the new goal",
"target_date": "2024-12-31",
"target_time": "23:59:00",
"completed": false,
"created_at": "2024-07-25T14:30:00Z",
"updated_at": "2024-07-25T14:30:00Z"
} |  |
| board/lifelist/int:pk/ |  | 선택한 LifeList 항목을 반환 | GET | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>
2.  응답
성공시
200 ok
{
"id": 1,
"user": 1,
"goal": "Test Goal",
"description": "Description of the test goal",
"target_date": "2024-12-31",
"target_time": "23:59:00",
"completed": false,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:00:00Z"
} |  |
| board/lifelist/int:pk/ |  | 특정 LifeList 항목을 업데이트 | PUT | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Content-Type: application/json
Authorization: Bearer <access_token>
Body : raw(json)
{
"goal": "Updated Goal",
"description": "Updated description of the goal",
"target_date": "2024-11-30",
"target_time": "22:00:00",
"completed": true
}
2.  응답
성공시
200 ok
{
"id": 1,
"user": 1,
"goal": "Updated Goal",
"description": "Updated description of the goal",
"target_date": "2024-11-30",
"target_time": "22:00:00",
"completed": true,
"created_at": "2024-07-25T14:00:00Z",
"updated_at": "2024-07-25T14:40:00Z"
} |  |
| board/lifelist/int:pk/ |  | 특정 LifeList 항목을 삭제 | DELETE | 1.요청:
Header : Authorization
Auth type : Bearer Token
Token에 로그인할 당시에 받았던 access토큰(로그인 성공시 반환값인 “access: “에 해당하는 부분) 넣기
-입력예시
Authorization: Bearer <access_token>
2.  응답
성공시
204 No Content |  |
