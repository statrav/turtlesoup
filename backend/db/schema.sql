-- 문제 테이블
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    description TEXT,
    answer TEXT,
    difficulty TEXT,
    category TEXT
);

-- 유저 질문 기록 테이블
CREATE TABLE user_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    problem_id INTEGER,
    question TEXT,
    ai_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(problem_id) REFERENCES problems(id)
);
