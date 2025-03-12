import sqlite3
import json
import argparse
import os

# argparse로 CLI 인자 처리
parser = argparse.ArgumentParser()
parser.add_argument("--jsonl_path", type=str, required=True)
args = parser.parse_args()

# DB 경로
db_path = "backend/db/ai_turtle.db"

# DB 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# JSONL 파일 읽고 DB에 삽입
count = 0
if not os.path.exists(args.jsonl_path):
    print(f"지정한 JSONL 파일을 찾을 수 없습니다: {args.jsonl_path}")
else:
    with open(args.jsonl_path, "r", encoding="utf-8") as file:
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
