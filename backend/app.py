from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

# model_handler import
from models.model_handler import get_response_from_model, explain_reasoning, judge_final_answer

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용 전체 허용 (배포 시 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic 모델
class QuestionRequest(BaseModel):
    problem_id: int
    user_id: str
    question: str

class HintRequest(BaseModel):
    problem_id: int
    user_id: str
    question: str

# ✅ 문제 리스트 전체 조회
@app.get("/problems")
def get_problems():
    conn = sqlite3.connect("db/ai_turtle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, difficulty, category FROM problems")
    rows = cursor.fetchall()
    conn.close()

    problems = []
    for row in rows:
        problems.append({
            "id": row[0],
            "title": row[1],
            "difficulty": row[2],
            "category": row[3]
        })
    return {"problems": problems}


# ✅ 문제 상세 조회 (문제 설명 포함)
@app.get("/problems/{problem_id}")
def get_problem_detail(problem_id: int):
    conn = sqlite3.connect("db/ai_turtle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, answer, difficulty, category FROM problems WHERE id = ?", (problem_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "문제를 찾을 수 없습니다."}

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "answer": row[3],
        "difficulty": row[4],
        "category": row[5]
    }


# ✅ 질문 처리 API
@app.post("/ask")
def ask_question(data: QuestionRequest):
    conn = sqlite3.connect("db/ai_turtle.db")
    cursor = conn.cursor()

    # 문제 설명 + 답 불러오기
    cursor.execute("SELECT description, answer FROM problems WHERE id = ?", (data.problem_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "문제를 찾을 수 없습니다."}

    problem_desc, problem_answer = row

    # 모델 처리
    ai_response = get_response_from_model(problem_desc, problem_answer, data.question)

    # 질문 기록 저장
    cursor.execute("""
        INSERT INTO user_questions (user_id, problem_id, question, ai_response)
        VALUES (?, ?, ?, ?)
    """, (data.user_id, data.problem_id, data.question, ai_response))

    conn.commit()
    conn.close()

    return {
        "response": ai_response,
        "message": f"AI의 응답: {ai_response}"
    }

class FinalAnswerRequest(BaseModel):
    problem_id: int
    user_id: str
    final_answer: str

@app.post("/submit_answer")
def submit_answer(data: FinalAnswerRequest):
    conn = sqlite3.connect("db/ai_turtle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT description, answer FROM problems WHERE id = ?", (data.problem_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "문제를 찾을 수 없습니다."}

    problem_desc, correct_answer = row
    is_correct, reasoning = judge_final_answer(problem_desc, correct_answer, data.final_answer)

    return {
        "is_correct": is_correct,
        "message": "정답입니다! 🎉" if is_correct else "틀렸습니다. 😢",
        "correct_answer": correct_answer if is_correct else None,
        "reasoning": reasoning
    }

@app.post("/hint")
def get_hint(data: HintRequest):
    conn = sqlite3.connect("db/ai_turtle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT description, answer FROM problems WHERE id = ?", (data.problem_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "문제를 찾을 수 없습니다."}

    problem_desc, problem_answer = row
    hint = explain_reasoning(problem_desc, problem_answer, data.question)

    return {"hint": hint}