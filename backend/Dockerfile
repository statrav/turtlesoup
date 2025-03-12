# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 코드 복사
COPY . /app

# 패키지 설치
RUN pip install --upgrade pip \
    && pip install fastapi uvicorn pandas transformers torch dotenv openai

# 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
