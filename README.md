# 🐢 TurtleSoup - 바다거북 스프 게임 웹 플랫폼

## 게임 설명
나폴리탄 괴담 계열의 수수께끼로, 추리게임의 일환이다. 다양한 카테고리와 난이도의 추리게임을 즐길 수 있다.

## 구성
- FastAPI Backend (LLM 기반)
- Nginx Frontend
- SQLite Database
- Docker Compose 관리

## 실행 방법
1. `.env` 파일에 OpenAI API 키 입력
2. `docker-compose up --build`

## 주요 기능
- 문제 리스트 / 상세 조회
- AI 예/아니오 추론
- 사용자 질문 및 정답 제출
- 포기 시 정답 노출 + 해설

## 향후 확장
- LLM 교체 (Claude, Gemini 등)
- 히스토리 저장
- 사용자 계정 시스템
