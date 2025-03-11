import sqlite3
import json

# JSONL 파일 경로
jsonl_path = "data/problems.jsonl"

# DB 연결
conn = sqlite3.connect("backend/db/ai_turtle.db")
cursor = conn.cursor()

# JSONL 읽고 DB에 삽입
with open(jsonl_path, "r", encoding="utf-8") as file:
    count = 0
    for line in file:
        if not line.strip():  # 빈 줄 무시
            continue
        problem = json.loads(line)
        cursor.execute("""
            INSERT INTO problems (title, description, answer, difficulty, category)
            VALUES (?, ?, ?, ?, ?)
        """, (
            problem["title"],
            problem["description"],
            problem["answer"],
            problem["difficulty"],
            problem["category"]
        ))
        count += 1

conn.commit()
conn.close()

print(f"{count}개의 문제가 성공적으로 삽입되었습니다.")

