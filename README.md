# DREAM CATCHER

🦁 멋쟁이 사자처럼 12기 중앙해커톤 성신여대 2팀 백앤드 페이지

## Project Introduction

학교를 떠나 사회로 나가게 되었을 때 우리는 어디로 가게 될까요? 내가 가고 싶은 곳에, 내가 하고 싶은 일을 하며 살 수 있을까요? 가끔 세상은 노력이라는 이름 아래 우리를 괴롭게 하고 숨게 만듭니다. 우리는 성공했을 때 삶을 배웠지만 실패했을 때의 삶은 찾지 못했습니다. 다시 용기를 내기 위해, 그리고 타인에게 용기를 주기 위해 우리는 **DREAM CATCHER**를 만듭니다. 

인생의 중요한 이정표를 정해진 시기에 달성해야 한다는 한국 사회의 기대가 경기 침체, 고용률이 낮은 상황과 맞물리면서 젊은이들의 불안을 증폭시킵니다.
한국 보건복지부 자료에 따르면 한국 19-34세 청년 중 5%인 54만명이 고립, 은둔 상태에 있다. 그 이유는 취업난(24.1%), 대인관계문제(23.5%), 가족 문제(12.4%), 건강 문제(12.4%) 등 이 이유들은 쉬었음 청년을 만듭니다. 
청년들은 취업에 어려움을 겪고, 가족들의 기대는 무겁고, 그들은 점차 스스로 할 수 있는 일에 대한 의문을 갖게 됩니다. 그렇게 그들은 무기력해지며, 은둔, 고립 청년들이 증가하는 현실로 이어집니다.

무기력해진 사람들에게 가장 어려운 일은 해야 하는 일을 제때 해내는 일이며, 제 때에 밥을 먹고, 운동하고 청소하고 샤워하는 가장 기초적인 삶의 습관들을 지키는 것입니다.

그래서 우리는 그들에게 자신을 투영한 드림파트너와 함께 가장 기초적인 어느 하루를 기록하고, 에브리스트와 라이프 리스트를 통해 하루의 목표와 삶의 목표를 반짝이는 별로 성장시키도록 돕고자 이 어플을 만들기 시작하였습니다.

## Development Period

2024.07.09 ~ 2024.08.06

## Tech Stack

- **Backend Framework**: Django DRF
- **Database**: SQLite
- **Server**: AWS EC2
- **Web Server**: Nginx
- **SSL**: Let's Encrypt


### API Documentation

| Endpoint                                 | Description                                 | Method | Header                         | Request Body | Response                                                                                                                                                                                                                     |
|-------------------------------------------|--------------------------------------|--------|----------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| home/                                     | 홈 화면                               | POST   |                            |          |                                                                                                                                                                                                                              |
| X                                         | 모든 리스트 가져오기                   | GET    | Authorization: Bearer Token|          | 200 OK: { "everylist": [...], "lifelist": [...] }<br>401 Unauthorized: 인증되지 않은 사용자<br>403 FORBIDDEN : 접근 권한이 없는 사용자                                                |
| notifications/                            | 모든 알림 조회                         | GET    | Authorization: Bearer Token|          | 200 OK: [ { "id": 1, "user": 1, "post": 5, "message": "user1님이 ...", "created_at": "2024-07-24T12:34:56Z", "read": false }, { ... } ]                                                  |
| notifications/mark_as_read/int:pk/        | 알림을 읽음 상태로 변경                | POST   | Authorization: Bearer Token<br>Content-Type: application/json |          | 200 OK: { "message": "Notification marked as read" }<br>404 Not Found: { "detail": "Not found." }<br>401 Unauthorized: { "detail": "Authentication credentials were not provided." }<br>403 Forbidden: { "detail": "You do not have permission to perform this action." } |
| signup/                                   | 회원가입                               | POST   |                            | form-data: { "user_id": "아이디", "username": "이름", "password": "비밀번호", "email": "이메일", "photo": "사진" } | 201 Created: { "message": "회원가입 성공" }                                                                                                                                                                                   |
| check_user_id/                            | 아이디 중복 확인                       | POST   |                            | form-data: { "user_id": "아이디" } | 200 OK: { "user_id_exists": true/false }                                                                                                                                                                                     |
| login/                                    | 로그인                                 | POST   |                            | form-data: { "user_id": "아이디", "password": "비밀번호" } | 200 OK: { "message": "로그인 성공", "refresh": "...", "access": "..." }                                                                                                                                                      |
| delete-account/                           | 계정 삭제                              | DELETE | Authorization: Bearer Token|          | 200 OK: { "message": "계정 삭제 성공" }                                                                                                                                                                                       |
| logout/                                   | 로그아웃                               | POST   | Authorization: Bearer Token|          | 200 OK: { "message": "로그아웃 성공" }                                                                                                                                                                                        |
| profile-edit/                             | 프로필 수정                            | POST   | Authorization: Bearer Token| form-data: { "username": "닉네임", "photo": "사진" } | 200 OK: { "message": "프로필이 성공적으로 수정되었습니다." }                                                                                                                                                                    |
| personal-info-edit/                       | 개인정보 수정                          | POST   | Authorization: Bearer Token| form-data: { "user_id": "아이디", "username": "이름", "password": "비밀번호", "password2": "비밀번호 확인", "email": "이메일" } | 200 OK: { "message": "프로필이 성공적으로 수정되었습니다." }                                                                                                                                                                    |
| password-reset-request/                   | 비밀번호 재설정을 위한 이메일 요청       | POST   |                            | raw(json): { "email": "20211307@sungshin.ac.kr" } | 200 OK: { "email": "20211307@sungshin.ac.kr" }<br>404 Not Found: { "error": "해당 이메일 주소가 없습니다." }                                                                                                                   |
| password-reset-confirm/                   | 비밀번호 재설정 확인                    | POST   |                            | raw(json): { "email": "20211307@sungshin.ac.kr", "new_password1": "3333", "new_password2": "3333" } | 200 OK: { "message": "비밀번호 재설정 성공" }<br>404 Not Found: { "error": "해당 이메일 주소가 없습니다." }                                                                                                                    |
| user/                                     | 사용자 정보 조회                        | GET    | Authorization: Bearer Token|          | 200 OK: { "id": 6, "user_id": "kkkknnnn", "username": "포포", "email": "34527865@naver.com", "photo_url": "https://dreamcatcherrr.store/myproject/media/default-profile.jpg", "profile": { "age": null } }                      |
| characters/                               | 캐릭터 생성                             | POST   | Authorization: Bearer Token| raw(json): { "name": "My Parrot", "type": "parrot" } | 201 Created: { "id": 3, "user": 3, "name": "My Parrot", "type": "parrot", "gauge": 0, "active": true }                                                                                                                        |
| characters/                               | 캐릭터 정보 조회                        | GET    | Authorization: Bearer Token|          | 200 OK: [ { "id": 1, "user": 1, "name": "my parrot", "type": "parrot", "gauge": 0, "active": true } ]                                                                                                                         |
| characters/<character_id>/                | 캐릭터 타입 변경                        | PATCH  | Authorization: Bearer Token| raw(json): { "type": "dolphin" } | 200 OK: { "id": 1, "user": 1, "name": "my parrot", "type": "dolphin", "gauge": 0, "active": true }                                                                                                                            |
| journal_entries/                          | 캐릭터 키우기(먹기)                         | POST   | Authorization: Bearer Token| raw(json): { "character": 1, "action_type": "eat", "meal_time": "breakfast", "action_detail": "시리얼과 우유", "completed": true } | 201 Created: { "id": 2, "character": 1, "date": "2024-07-23", "action_type": "eat", "meal_time": "breakfast", "action_detail": "시리얼과 우유", "completed": false }                                                          |
| journal_entries/                          | 캐릭터 키우기(씻기)                        | POST   | Authorization: Bearer Token| raw(json): { "character": 1, "action_type": "eat", "meal_time": "breakfast", "action_detail": "시리얼과 우유", "completed": true } | 201 Created: { "id": 2, "character": 1, "date": "2024-07-23", "action_type": "eat", "meal_time": "breakfast", "action_detail": "시리얼과 우유", "completed": false }                                                          |
| journal_entries/                          | 캐릭터 키우기                         | POST   | Authorization: Bearer Token| {
   "character": 1,  // 캐릭터 ID
   "action_type": "wash",
   "completed": true  // 예: True 아니오: False
} | 201 created
{
   "id": 3,
   "character": 1,
   "date": "2024-07-23",
   "action_type": "wash",
   "meal_time": null,
   "action_detail": null,
   "completed": true
}                                                          |
| journal_entries/                          | 캐릭터 키우기(운동하기)                         | POST   | Authorization: Bearer Token| {
   "character": 1,   // 캐릭터 ID
   "action_type": "walk",
   "action_detail": "배드민턴", //뭔 운동했는지
   "completed": true
}| 201 created
{
   "id": 7,
   "character": 1,  
   "date": "2024-07-23",
   "action_type": "walk",
   "meal_time": null,
   "action_detail": "베란다",
   "completed": true
}                                                           |
| journal_entries/                          | 캐릭터 키우기(청소하기)                         | POST   | {
   "character": 1,  // 캐릭터 ID
   "action_type": "cleaning",
   "action_detail": "방", //어딜 청소했는지
   "completed": true
} | 201 created
{
   "id": 8,
   "character": 1,
   "date": "2024-07-23",
   "action_type": "clean",
   "meal_time": null,
   "action_detail": "방",
   "completed": true
} 
| characters/<character_id>/records/<date>/ | 일별 먹기 기록 조회                     | GET    | Authorization: Bearer Token|          | 200 OK: { "date": "2024-08-05", "day": "Monday", "meals": { "breakfast": [ "시리얼과 우유" ], "lunch": [ "콩나물국밥", "토스트" ], "dinner": [ "순두부찌개", "밥", "스테이크" ], "snack": [ "젤리", "우유", "빵" ] } }          |
| recommendations/random/                   | 랜덤 추천                               | GET    | Authorization: Bearer Token|          | 200 OK: { "foods": [ "아이스크림빙수", "해물전", "부추전" ], "cleaning_spots": [ "주방 서랍", "차고", "재활용품 정리함" ], "walking_places": [ "서핑", "자이로토닉", "골프" ] }                                                |
| recommendations/keyword/                  | 키워드 기반 추천                       | GET    | Authorization: Bearer Token|          | 200 OK: { "foods": [ "장조림", "연근조림", "조개탕", "조개구이", "조기매운탕", "코다리조림", "조기구이", "우엉조림", "연근조림", "조개탕", "조개구이", "조기매운탕", "코다리조림", "조기구이", "우엉조림", "고등어조림", "연근조림" ], "cleaning_spots": [], "walking_places": [ "조깅", "체조" ] } |
| characters/gauge/                         | 캐릭터 게이지 조회                       | GET    | Authorization: Bearer Token|          | 200 OK: { "gauge": 40 }                                                                                                                                                                                                      |
| user-activity-dates/                      | 활동 날짜 조회                          | GET    | Authorization: Bearer Token|          | 200 OK: [ "2024-07-30" ]                                                                                                                                                                                                     |
| diary_entries/                            | 일기 작성                               | POST   | Authorization: Bearer Token| raw(json): { "character": 1, "weather": "sunny", "diary_text": "오늘은 날씨가 좋았다." } | 201 Created: { "id": 3, "character": 1, "date": "2024-07-24", "weather": "sunny", "diary_text": "오늘은 날씨가 좋았다." }                                                                                                     |
| characters/end/                           | 캐릭터 비활성화                          | POST   | Authorization: Bearer Token|          | 200 OK: { "message": "Character has been ended." }                                                                                                                                                                            |
| characters/<int:character_id>/ending/     | 캐릭터 엔딩 조회                        | GET    | Authorization: Bearer Token|          | 200 OK: [ { "date": "2024-08-05", "day": "Monday", "weather": "cloudy", "meals": { "breakfast": [ "시리얼과 우유", "빵" ], "lunch": [ "설렁탕", "주스", "껌" ], "dinner": [ "닭도리탕", "단무지" ], "snack": [ "스타벅스 케이크", "우유", "사탕", "젤리" ] }, "records": { "cleaning": [], "exercise": [], "shower": [] }, "diary": "날씨 배드." } ] |
| characters/<id>/journal/<date>/ | 특정 날짜 클릭시 그때 행동기록, 일기기록 보기 | GET | Authorization: Bearer Token | | 200 OK: { "date": "2024-07-25", "day": "Thursday", "weather": "sunny", "meals": { "breakfast": "시리얼과 우유", "lunch": "요거트", "dinner": "바게트", "snack": "뿡" }, "records": { "cleaning": "거실", "exercise": "배드민턴과 탁구", "shower": { "completed": false } }, "diary": "에어컨이 고장나서 너무 더웠다.." } |
| api/token/ | JWT token 얻기 위한 링크 | POST | Authorization: Bearer Token | raw(json): { "username": "사용자 이름 (Text)", "password": "비밀번호 (Text)" } | 200 OK: { "refresh": "리프레시 토큰 (Text)", "access": "액세스 토큰 (Text)" } |
| api/token/refresh/ | Refresh JWT token | POST | Authorization: Bearer Token | raw(json): { "refresh": "리프레시 토큰 (Text)" } | 200 OK: { "access": "액세스 토큰 (Text)" } |
| post/create/ | 게시물 생성 | POST | Authorization: Bearer Token | raw(json): { "content": "새로운 게시물 내용", "image": null } | 201 CREATED: { "message": "Post created successfully" }<br>403 FORBIDDEN: { "message": "You are banned from posting until YYYY-MM-DD HH:MM:SS" } |
| post/like/int:pk/ | 게시물 좋아요 | POST | Authorization: Bearer Token | | 200 OK: { "liked": "좋아요 상태 (true 또는 false)", "total_likes": "좋아요 총 개수" } |
| post/posthome/ | 게시물 조회 | GET | | 쿼리 파라미터: sort (선택 사항): 정렬 기준 ('date' 또는 'likes')<br>category (선택 사항): 게시물 카테고리 ('latest', 'my_posts', 'liked_posts') | 200 OK: [ { "id": 1, "content": "This is a sample post", "image": "http://example.com/media/post_images/sample.jpg", "date_posted": "2024-08-05T12:34:56Z", "author_username": "john_doe", "author_profile": { "profile_image": "http://example.com/media/profile_images/john_doe.jpg" }, "likes": [2, 3, 4], "total_likes": 3 }, { "id": 2, "content": "Another sample post", "image": null, "date_posted": "2024-08-04T11:22:33Z", "author_username": "jane_smith", "author_profile": { "profile_image": "http://example.com/media/profile_images/jane_smith.jpg" }, "likes": [1, 2], "total_likes": 2 } ] |
| post/update/<int:pk>/ | 게시물 수정 | PATCH | Authorization: Bearer Token | raw(json): { "title": "제목 (선택 사항)", "content": "내용 (선택 사항)" } | 200 OK: { "message": "게시물 수정 성공" }<br>403 FORBIDDEN: { "message": "Unauthorized" } |
| post/delete/int:pk/ | 게시물 삭제 | DELETE | Authorization: Bearer Token | | 200 OK: { "message": "게시물 삭제 성공" }<br>403 FORBIDDEN: { "message": "Unauthorized" } |
| post/int:pk/posts | 사용자 게시물 목록 | GET | Authorization: Bearer Token | | 200 OK: [ { "id": "게시물 ID", "title": "제목", "content": "내용", "author": "작성자", "date_posted": "작성일", "total_likes": "좋아요 수" }, ... ] |
| post/int:pk/ | 게시물 상세보기 | GET | | | 200 OK: { "id": "게시물 ID", "title": "제목", "content": "내용", "author": "작성자", "date_posted": "작성일", "total_likes": "좋아요 수" } |
| post/notifications/read/int:pk/ | 특정 알림을 읽음 상태로 변경 | POST | Authorization: Bearer Token | | 200 OK: { "message": "Notification marked as read" }<br>403 FORBIDDEN: { "message": "Notification not found" }<br>404 Not Found: { "message": "Notification not found" } |
| post/like/int:pk/ | 특정 게시글을 좋아요하거나 좋아요를 취소 | POST | Authorization: Bearer Token | | 200 OK: { "liked": true, "total_likes": 10 }<br>200 OK, Unliked: { "liked": false, "total_likes": 9 }<br>403 FORBIDDEN: { "message": "Post not found" }<br>404 Not Found: { "message": "Unauthorized" } |
| post/report_post/int:pk/ | 특정 게시물을 신고 | POST | Authorization: Bearer Token | | 200 OK: { "message": "Post reported successfully" }<br>400 Bad Request: { "message": "You have already reported this post." } |
| board/recommend/ | 추천목록을 만드는 링크 | POST | Authorization: Bearer Token | raw(json): { "character_id": 1 } | 200 OK: { "recommendations": "추천 리스트 (Array)" } |
| board/recommend_page/ | 추천 페이지 | GET | Authorization: Bearer Token | | 200 OK: { "message": "게시물 삭제 성공" }<br>403 FORBIDDEN: { "message": "Unauthorized" } |
| board/add_recommendations/ | 추천된 항목들을 선택하여 에브리리스트에 추가 | POST | Authorization: Bearer Token | raw(json): { "recommendations": [ "책 읽기", "명상하기", "음악 듣기" ] } | 200 OK: { "success": "Recommendations added to your EveryList" } |
| board/everylist/ | 현재 사용자의 모든 EveryList 항목을 반환 | GET | Authorization: Bearer Token | | 200 OK: [ { "id": 1, "user": 1, "task": "Test Task", "due_date": "2024-07-25", "due_time": "15:00:00", "completed": false, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:00:00Z" }, ... ] |
| board/everylist/ | 새로운 EveryList 항목을 생성 | POST | Authorization: Bearer Token<br>Content-Type: application/json | raw(json): { "task": "New Task", "due_date": "2024-07-26", "due_time": "14:30:00", "completed": false } | 201 Created: { "id": 2, "user": 1, "task": "New Task", "due_date": "2024-07-26", "due_time": "14:30:00", "completed": false, "created_at": "2024-07-25T14:30:00Z", "updated_at": "2024-07-25T14:30:00Z" } |
| board/everylist/int:pk/ | 선택한 EveryList 항목을 반환 | GET | Authorization: Bearer Token | | 200 OK: { "id": 1, "user": 1, "task": "Test Task", "due_date": "2024-07-25", "due_time": "15:00:00", "completed": false, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:00:00Z" } |
| board/everylist/int:pk/ | EveryList 항목을 업데이트 | PUT | Authorization: Bearer Token<br>Content-Type: application/json | raw(json): { "task": "Updated Task", "due_date": "2024-07-27", "due_time": "16:00:00", "completed": true } | 200 OK: { "id": 1, "user": 1, "task": "Updated Task", "due_date": "2024-07-27", "due_time": "16:00:00", "completed": true, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:40:00Z" } |
| board/everylist/int:pk/ | 특정 EveryList 항목을 삭제 | DELETE | Authorization: Bearer Token | | 204 No Content |
| board/lifelist/ | 현재 사용자의 모든 LifeList 항목을 반환 | GET | Authorization: Bearer Token | | 200 OK: [ { "id": 1, "user": 1, "goal": "Test Goal", "description": "Description of the test goal", "target_date": "2024-12-31", "target_time": "23:59:00", "completed": false, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:00:00Z" }, ... ] |
| board/lifelist/ | 새로운 LifeList 항목을 생성 | POST | Authorization: Bearer Token<br>Content-Type: application/json | raw(json): { "goal": "New Goal", "description": "Description of the new goal", "target_date": "2024-12-31", "target_time": "23:59:00", "completed": false } | 201 Created: { "id": 2, "user": 1, "goal": "New Goal", "description": "Description of the new goal", "target_date": "2024-12-31", "target_time": "23:59:00", "completed": false, "created_at": "2024-07-25T14:30:00Z", "updated_at": "2024-07-25T14:30:00Z" } |
| board/lifelist/int:pk/ | 선택한 LifeList 항목을 반환 | GET | Authorization: Bearer Token | | 200 OK: { "id": 1, "user": 1, "goal": "Test Goal", "description": "Description of the test goal", "target_date": "2024-12-31", "target_time": "23:59:00", "completed": false, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:00:00Z" } |
| board/lifelist/int:pk/ | 특정 LifeList 항목을 업데이트 | PUT | Authorization: Bearer Token<br>Content-Type: application/json | raw(json): { "goal": "Updated Goal", "description": "Updated description of the goal", "target_date": "2024-11-30", "target_time": "22:00:00", "completed": true } | 200 OK: { "id": 1, "user": 1, "goal": "Updated Goal", "description": "Updated description of the goal", "target_date": "2024-11-30", "target_time": "22:00:00", "completed": true, "created_at": "2024-07-25T14:00:00Z", "updated_at": "2024-07-25T14:40:00Z" } |
| board/lifelist/int:pk/ | 특정 LifeList 항목을 삭제 | DELETE | Authorization: Bearer Token | | 204 No Content |


## Collaborators

- 🦁 **김나영** - [GitHub Profile](https://github.com/nnaX000/)

- 🦁 **전해성** - [GitHub Profile](https://github.com/suncastle023)
