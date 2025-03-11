let selectedProblemId = null;

window.onload = () => {
    fetchProblems();
};

function fetchProblems() {
    fetch("http://172.16.200.83:8000/problems")  // ← 여긴 실제 백엔드 IP에 맞게 유지
        .then(response => response.json())
        .then(data => {
            const problems = data.problems;
            const list = document.getElementById("problems");

            // 기존 목록 초기화
            list.innerHTML = '';

            problems.forEach(problem => {
                const li = document.createElement("li");
                li.textContent = `[${problem.difficulty}] ${problem.title} (${problem.category})`;
                li.style.cursor = "pointer";
                li.onclick = () => selectProblem(problem.id, problem.title);
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error("문제 리스트 로딩 실패", err);
        });
}

function selectProblem(id, title) {
    selectedProblemId = id;
    document.getElementById("problem-title").textContent = title;

    // 문제 설명 불러오기 (신규 /problems/{id} API 사용)
    fetch(`http://172.16.200.83:8000/problems/${id}`)
        .then(response => response.json())
        .then(problem => {
            document.getElementById("problem-description").textContent = problem.description;
        })
        .catch(err => {
            console.error("문제 설명 로딩 실패", err);
        });

    // 질문 입력창 보이기
    document.getElementById("question-section").style.display = "block";
    document.getElementById("response").textContent = "";
    document.getElementById("user-question").value = "";
}

function submitQuestion() {
    const question = document.getElementById("user-question").value;
    if (!question || !selectedProblemId) return;

    fetch("http://172.16.200.83:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem_id: selectedProblemId,
            user_id: "demo_user",
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").textContent = `AI 응답: ${data.response}`;
    })
    .catch(err => {
        console.error("질문 전송 실패", err);
        document.getElementById("response").textContent = "오류가 발생했습니다. 다시 시도해주세요.";
    });
}

function giveUp() {
    fetch(`http://172.16.200.83:8000/problems/${selectedProblemId}`)
        .then(response => response.json())
        .then(problem => {
            const result = `정답을 알려드릴게요! ${problem.answer}`;
            document.getElementById("response").textContent = result;
        });
}

function submitFinalAnswer() {
    const userFinalAnswer = document.getElementById("final-answer").value;
    if (!userFinalAnswer || !selectedProblemId) return;

    fetch("http://172.16.200.83:8000/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            problem_id: selectedProblemId,
            user_id: "demo_user",
            final_answer: userFinalAnswer
        })
    })
    .then(response => response.json())
    .then(data => {
        let msg = data.message;
        if (data.is_correct) {
            msg += `\n\n정답: ${data.correct_answer}`;
        }
        document.getElementById("response").textContent = msg;
    });
}

function fetchProblems() {
    document.getElementById("loading-msg").style.display = "block";
    
    fetch("http://172.16.200.83:8000/problems")
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading-msg").style.display = "none";

            const problems = data.problems;
            const list = document.getElementById("problems");
            list.innerHTML = '';
            problems.forEach(problem => {
                const li = document.createElement("li");
                li.textContent = `[${problem.difficulty}] ${problem.title} (${problem.category})`;
                li.onclick = () => selectProblem(problem.id, problem.title);
                list.appendChild(li);
            });
        })
        .catch(err => {
            document.getElementById("loading-msg").textContent = "문제 리스트 로딩 실패 😢";
            console.error(err);
        });
}
