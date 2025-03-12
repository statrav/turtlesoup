import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_response_from_model(problem_desc, problem_answer, question):
    prompt = f"""
문제: {problem_desc}
정답: {problem_answer}
질문: {question}

위 질문은 정답 유도에 어떤 역할을 하나요?
다음 중 하나로 답변해 주세요: "예", "아니오", "무관함"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": "당신은 추리게임 바다거북스프 게임의 진행자입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        result_text = response.choices[0].message.content.strip()
        if "예" in result_text[:5]:
            return "예"
        elif "아니오" in result_text[:5]:
            return "아니오"
        elif "무관" in result_text[:5]:
            return "무관함"
        else:
            return "무관함"
    except Exception as e:
        print(f"[GPT Error] {e}")
        return "오류가 발생하였습니다. 관리자에게 문의하세요."

def explain_reasoning(problem_desc, problem_answer, question):
    prompt = f"""
문제: {problem_desc}
정답: {problem_answer}
질문: {question}

사용자가 질문을 통해 정답을 유추할 수 있도록 도움을 주세요.
단, 정답을 알려주면 안됩니다. 
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": "당신은 추론 과정을 돕는 전문 AI입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT Reasoning Error] {e}")
        return "설명 생성에 실패하였습니다."
    
def judge_final_answer(problem_desc, correct_answer, user_answer):
    prompt = f"""
문제: {problem_desc}
정답: {correct_answer}
사용자 제출 답변: {user_answer}

이 사용자의 제출 답변이 정답과 의미상으로 동일한가요?  
"예" 또는 "아니오"로만 답해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 정답 검증 AI입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        full_response = response.choices[0].message.content.strip()
        is_correct = full_response.startswith("예")
        return is_correct, full_response
    except Exception as e:
        print(f"[GPT FinalAnswer Judge Error] {e}")
        return False, "판별 실패"


# problem_desc = "한 남자가 고층 아파트 10층에 살고 있다. 아침마다 엘리베이터를 타고 1층까지 편히 내려가며 하루를 시작한다. 하지만 이상하게도, 집으로 돌아올 땐 항상 7층에서 내려 나머지 3층을 계단으로 올라간다. 운동을 좋아하는 성격도 아니다. 도대체 왜 이런 수고스러운 행동을 반복하는 걸까?"
# problem_answer = "그는 키가 너무 작아서 10층 버튼에 손이 닿지 않는다. 7층 버튼까지만 겨우 닿기 때문에 엘리베이터를 7층까지만 타고, 이후 계단을 이용하는 것이다. 다른 사람과 함께 타거나, 우산처럼 길쭉한 물건을 들고 있을 때만 10층 버튼을 누를 수 있다."
# question = "키와 관련이 있나?"

# print("#####answer#####")
# print(get_response_from_model(problem_desc, problem_answer, question))
# print("#####reasoning#####")
# print(explain_reasoning(problem_desc, problem_answer, question))