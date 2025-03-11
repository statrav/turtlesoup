from transformers import pipeline

# 모델 로딩 (처음 1회만 시간이 좀 걸림)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 예/아니오/무관함 분류 라벨
labels = ["예", "아니오", "무관함"]

def get_response_from_model(problem_desc, problem_answer, question):
    """
    문제 설명 + 정답 + 질문 → AI가 예/아니오/무관함 중 하나를 판단
    """
    prompt = f"문제: {problem_desc}\n정답: {problem_answer}\n질문: {question}"

    result = classifier(prompt, candidate_labels=labels)
    top_label = result["labels"][0]

    return top_label
